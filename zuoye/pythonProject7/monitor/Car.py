import requests
import base64
import cv2 as cv


# opencv 图片
def vehicle_detect(img):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    params = {"image": base64_image}
    access_token = '24.4e5b7c103182469ecb6454bfb6862f87.2592000.1722824706.282335-91292523'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    num = 0
    if response:
        data = response.json()
        num = 0
        if 'words_result' in data:
            for result in data['words_result']:
                num += 1
                number = result.get('number', '')
                vertices = result.get('vertexes_location', [])

                # 检查 vertices 是否有四个点
                if len(vertices) == 4:
                    # Extract the coordinates of the rectangle
                    x1 = vertices[0]['x']
                    y1 = vertices[0]['y']
                    x2 = vertices[2]['x']
                    y2 = vertices[2]['y']

                    # Draw the rectangle
                    cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    # Define the text properties
                    text = number
                    position = (x1, y1 - 10)
                    font = cv.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    color = (0, 0, 255)  # Red
                    thickness = 2

                    # Annotate the image with the license plate number
                    img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)
                else:
                    print("Vertices location data is not complete or malformed.")
        else:
            print("")

    return img, num

# 示例调用
# img = cv.imread('path_to_image.jpg')
# annotated_img, number_of_plates = vehicle_detect(img)




