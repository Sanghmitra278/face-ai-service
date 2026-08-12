import cv2

# Load image
image = cv2.imread("uploads/test.jpg")

if image is None:
    raise Exception("Image not found.")

h, w = image.shape[:2]

# Load detector
detector = cv2.FaceDetectorYN.create(
    model="onnx/yunet.onnx",
    config="",
    input_size=(w, h),
    score_threshold=0.8,
    nms_threshold=0.3,
    top_k=5000
)

# IMPORTANT: Set image size
detector.setInputSize((w, h))

# Detect faces
retval, faces = detector.detect(image)

print("Return Value:", retval)

if faces is None:
    print("No face detected.")
else:
    print(f"Faces detected: {len(faces)}")

    for i, face in enumerate(faces):
        print(f"\nFace {i+1}")

        x, y, width, height = face[:4]

        print("Bounding Box")
        print("x =", x)
        print("y =", y)
        print("width =", width)
        print("height =", height)

        print("\nComplete Output:")
        print(face)
        
	import cv2
	
	print(cv2.__version__)
	print(hasattr(cv2, "FaceDetectorYN"))
	print(hasattr(cv2, "FaceRecognizerSF"))
	
	# Load image
	image = cv2.imread("uploads/test.jpg")