import numpy as np

from services.scrfd_utils import (
    distance2bbox,
    distance2kps,
)

from services.nms import nms


class SCRFDDecoder:

    def __init__(
        self,
        input_size=(640, 640),
        conf_threshold=0.5,
        nms_threshold=0.45,
    ):

        self.input_size = input_size

        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold

        # SCRFD uses 3 feature maps
        self.strides = [8, 16, 32]

        # cache anchor centers
        self.center_cache = {}

    def get_anchor_centers(self, stride):
        """
        Generate anchor centers for one stride.
        """

        feat_h = self.input_size[1] // stride
        feat_w = self.input_size[0] // stride

        key = (feat_h, feat_w, stride)

        if key in self.center_cache:
            return self.center_cache[key]

        y, x = np.mgrid[:feat_h, :feat_w]

        centers = np.stack(
            (x, y),
            axis=-1
        ).astype(np.float32)

        centers = (centers + 0.5) * stride

        centers = centers.reshape(-1, 2)

        # SCRFD predicts 2 anchors per location
        centers = np.repeat(
            centers,
            2,
            axis=0,
        )

        print(f"Stride {stride} centers: {centers.shape}")

        self.center_cache[key] = centers

        return centers

    def decode_stride(
        self,
        scores,
        bboxes,
        kpss,
        stride,
    ):
        """
        Decode one SCRFD feature map.
        """

        centers = self.get_anchor_centers(stride)

        scores = scores.reshape(-1)
        print(f"\n===== STRIDE {stride} =====")
        print("Raw score :", scores[:10])

        bboxes = bboxes.reshape(-1, 4)
        print("\nFirst 5 raw bboxes")
        print(bboxes[:5])

        kpss = kpss.reshape(-1, 10)
        print("\nFirst 5 raw landmarks")
        print(kpss[:5])

        keep = scores > self.conf_threshold

        if keep.sum() == 0:
            return None

        scores = scores[keep]

        centers = centers[keep]

        bboxes = bboxes[keep] * stride

        kpss = kpss[keep] * stride

        boxes = distance2bbox(
            centers,
            bboxes,
        )
        print("\nFirst 5 decoded boxes")
        print(boxes[:5])

        landmarks = distance2kps(
            centers,
            kpss,
        )
        print("\nFirst landmark")
        print(landmarks[0])

        return (
            boxes,
            scores,
            landmarks,
        )

    def decode(self, outputs):
        """
        Decode complete SCRFD outputs.

        Parameters
        ----------
        outputs : list
            [
                score8,
                score16,
                score32,
                bbox8,
                bbox16,
                bbox32,
                kps8,
                kps16,
                kps32
            ]

        Returns
        -------
        dict
        """

        all_boxes = []
        all_scores = []
        all_landmarks = []

        for i, stride in enumerate(self.strides):

            result = self.decode_stride(
                outputs[i][0],
                outputs[i + 3][0],
                outputs[i + 6][0],
                stride,
            )

            if result is None:
                continue

            boxes, scores, landmarks = result

            all_boxes.append(boxes)
            all_scores.append(scores)
            all_landmarks.append(landmarks)

        if len(all_boxes) == 0:

            return {
                "boxes": np.empty((0, 4), dtype=np.float32),
                "scores": np.empty((0,), dtype=np.float32),
                "landmarks": np.empty((0, 5, 2), dtype=np.float32),
            }

        boxes = np.concatenate(all_boxes, axis=0)

        scores = np.concatenate(all_scores, axis=0)

        landmarks = np.concatenate(all_landmarks, axis=0)

        keep = nms(
            boxes,
            scores,
            self.nms_threshold,
        )

        boxes = boxes[keep]
        scores = scores[keep]
        landmarks = landmarks[keep]

        return {
            "boxes": boxes.astype(np.float32),
            "scores": scores.astype(np.float32),
            "landmarks": landmarks.astype(np.float32),
        }