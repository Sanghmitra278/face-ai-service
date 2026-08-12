'''import numpy as np


def distance2bbox(points, distance):
    """
    Decode bbox from point centers.

    Args:
        points : (N,2)
        distance : (N,4)

    Returns
        (N,4)
    """

    x1 = points[:, 0] - distance[:, 0]
    y1 = points[:, 1] - distance[:, 1]

    x2 = points[:, 0] + distance[:, 2]
    y2 = points[:, 1] + distance[:, 3]

    return np.stack((x1, y1, x2, y2), axis=-1)


def distance2kps(points, distance):
    """
    Decode 5 landmarks.
    """

    preds = []

    for i in range(5):
        px = points[:, 0] + distance[:, 2 * i]
        py = points[:, 1] + distance[:, 2 * i + 1]
        preds.append(px)
        preds.append(py)

    return np.stack(preds, axis=-1)'''
    
    
    
    
import numpy as np


def distance2bbox(points: np.ndarray,
                  distance: np.ndarray) -> np.ndarray:
    """
    Decode bounding boxes from SCRFD distance predictions.

    Args:
        points    : (N,2) anchor centers
        distance  : (N,4) [l,t,r,b]

    Returns:
        (N,4) -> x1,y1,x2,y2
    """

    x1 = points[:, 0] - distance[:, 0]
    y1 = points[:, 1] - distance[:, 1]

    x2 = points[:, 0] + distance[:, 2]
    y2 = points[:, 1] + distance[:, 3]

    return np.stack(
        [x1, y1, x2, y2],
        axis=1
    )


def distance2kps(points: np.ndarray,
                 distance: np.ndarray) -> np.ndarray:
    """
    Decode 5 facial landmarks.

    Args:
        points    : (N,2)
        distance  : (N,10)

    Returns:
        (N,5,2)
    """

    preds = []

    for i in range(5):

        px = points[:, 0] + distance[:, i * 2]
        py = points[:, 1] + distance[:, i * 2 + 1]

        preds.append(
            np.stack(
                [px, py],
                axis=1
            )
        )

    return np.stack(
        preds,
        axis=1
    )