import onnxruntime as ort

model_path = "onnx/scrfd_500m_bnkps.onnx"   # adjust if needed

session = ort.InferenceSession(
    model_path,
    providers=["CPUExecutionProvider"]
)

print("=" * 60)
print("INPUT")
print("=" * 60)

for i in session.get_inputs():
    print("Name :", i.name)
    print("Shape:", i.shape)
    print("Type :", i.type)
    print()

print("=" * 60)
print("OUTPUTS")
print("=" * 60)

for index, o in enumerate(session.get_outputs()):
    print(f"Output {index}")
    print("Name :", o.name)
    print("Shape:", o.shape)
    print("Type :", o.type)
    print()