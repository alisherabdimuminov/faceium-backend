from deepface import DeepFace


try:
    result = DeepFace.verify(
        img1_path = "img1.jpeg",
        img2_path = "img6.png",
        anti_spoofing=True,
    )
    print(result)
except Exception as e:
    cause = str(e.__cause__)
    context = str(e.__context__)
    print("cause", cause)
    print("context", context)
    print(e)