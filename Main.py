import cv2

capture = cv2.VideoCapture(0) #Tomo como device de captura la camara web

while (True):

    ret, frame = capture.read() #Leo un frame (de esta manera lea tan rapido como pueda no respeta fps)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #Cambio el frame a grayscale

    #for i in frame.shape()[1]:
    #    for j in frame.shape()[0]:
    #        sum += frame[i, j]

    #gray = cv2.putText(gray, str(sum), (int(frame.shape[1] / 2), int(frame.shape[0] / 2)), cv2.FONT_HERSHEY_COMPLEX, 1,
                      255)  # Pongo algun texto
    gray = cv2.putText(gray, "Hola", (int(frame.shape[1]/2), int(frame.shape[0]/2)), cv2.FONT_HERSHEY_COMPLEX, 1, 255) #Pongo algun texto

    cv2.imshow('gris', gray) #Muestro imagen en escala de grises
    cv2.imshow('original', frame) #Muestro imagen original


    if cv2.waitKey(1) == 27: #Espero la tecla para salir
        break

capture.release()
cv2.destroyAllWindows()