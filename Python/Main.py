import numpy as np
import cv2
import pytesseract as tess
import matplotlib.pyplot as plt
import FileHandling

#apretar q para salir
#apretar c para que trate de reconocer lo escrito


drawing = False
prevx, prevy = None,None

def draw_circle(event,x,y,flags,param):                 #FUNCION CALLBACK DE MANEJO DE EVENTOS DE MOUSE
    global drawing #Me dice si tengo el mouse apretado
    global prevx #Posicion x anterior
    global prevy #posicion y anterior
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:         #Cuando apreto el mouse, dibujo un circulo en el lugar
        drawing = True                         #y guardo la posicion
        img = cv2.circle(img,(x,y),1,(0,0,0), -1)
        prevx, prevy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:         #Cuando muevo el mouse, me fijo si el mouse sigue apretado
        if drawing == True:                    #Si lo esta, dibujo una linea desde la posiciona anterior a la actual
            img = cv2.line(img,(prevx, prevy),(x,y),(0, 0, 0), 2)
            prevx, prevy = x, y
    elif event == cv2.EVENT_LBUTTONUP:        #Cuando suelto el boton dibujo una ultima linea
        drawing = False
        img = cv2.line(img,(prevx, prevy),(x,y),(0, 0, 0), 2)
        prevx, prevy = None,None

img = (np.ones((300,600,3), np.uint8)*255)  #Creo una imagen necgra
cv2.namedWindow('Canvas')             #La llamo canvas
cv2.setMouseCallback('Canvas',draw_circle, img)  #Seteo los callbacks para el mouse
while True:
    cv2.imshow('Canvas',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(20) & 0xFF == ord('c'):

        boxes = tess.image_to_boxes(img, lang="equ")
        h, w, _ = img.shape
        if boxes:
            for b in boxes.splitlines():
                b = b.split(' ')
                img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
                print(b[0])
        else:
            print("nothing found")
            break
        while True:
            cv2.imshow('Canvas', img)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        break

    #elif cv2.waitKey(20) & 0xFF == ord('s'):
    #    img = cv2.resize(img, (50, 50))
    #    FileHandling.saveImage(img)
    #    break
plt.show()
cv2.destroyAllWindows()