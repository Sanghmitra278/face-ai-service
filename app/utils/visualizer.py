import cv2


def draw_result(image, result):

    img = image.copy()

    for box, score, kps in zip(result["boxes"], result["scores"], result["landmarks"]):
        x1, y1, x2, y2 = box.astype(int)

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            img,
            f"{score:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        for point in kps.astype(int):
            cv2.circle(img, tuple(point), 3, (0, 0, 255), -1)

    return img
