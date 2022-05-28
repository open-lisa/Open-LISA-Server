import Open_LISA_SDK


def main():
    sdk = Open_LISA_SDK.SDK(log_level="DEBUG")
    sdk.connect_through_RS232(baudrate=921600)

    instruments = sdk.list_instruments()
    camera = None
    for i in instruments:
        if i.ID == "CAM_ID":
            camera = i

    if camera:
        result = camera.send("get_image", "bytes")
        print("Saving image bytes...")
        with open("image.jpeg", "wb") as f:
            f.write(result)
    else:
        print("Camera with ID 'CAM_ID' not found")


if __name__ == "__main__":
    main()
