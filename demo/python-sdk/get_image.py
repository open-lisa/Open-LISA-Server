import Open_LISA_SDK

def main():
  sdk = Open_LISA_SDK.SDK()
  sdk.connect_through_RS232()

  instruments = sdk.list_instruments()
  cammera = None
  for i in instruments:
    if i.ID == "CAM_ID":
      cammera = i

  if cammera:
    result = cammera.send("get_image", "bytes")
    print("Saving image bytes...")
    with open("image.jpeg", "wb") as f:
      f.write(result)
  else:
    print("Cammera with ID 'CAM_ID' not found")

if __name__ == "__main__":
    main()