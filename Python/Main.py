import numpy as np
import cv2
import matplotlib.pyplot as plt
import FileHandling

drawing = False
prevx, prevy = None,None

def draw_circle(event,x,y,flags,param):                 #FUNCION CALLBACK DE MANEJO DE EVENTOS DE MOUSE
    global drawing #Me dice si tengo el mouse apretado
    global prevx #Posicion x anterior
    global prevy #posicion y anterior
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:         #Cuando apreto el mouse, dibujo un circulo en el lugar
        drawing = True                         #y guardo la posicion
        img = cv2.circle(img,(x,y),2,(255,255,255), -1)
        prevx, prevy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:         #Cuando muevo el mouse, me fijo si el mouse sigue apretado
        if drawing == True:                    #Si lo esta, dibujo una linea desde la posiciona anterior a la actual
            img = cv2.line(img,(prevx, prevy),(x,y),(255, 255, 255), 2)
            prevx, prevy = x, y
    elif event == cv2.EVENT_LBUTTONUP:        #Cuando suelto el boton dibujo una ultima linea
        drawing = False
        img = cv2.line(img,(prevx, prevy),(x,y),(255, 255, 255), 2)
        prevx, prevy = None,None

img = np.zeros((200,200), np.uint8)  #Creo una imagen negra
cv2.namedWindow('Canvas')             #La llamo canvas
cv2.setMouseCallback('Canvas',draw_circle, img)  #Seteo los callbacks para el mouse
while True:
    cv2.imshow('Canvas',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(20) & 0xFF == ord('s'):
        img = cv2.resize(img, (50, 50))
        FileHandling.saveImage(img)
        break
plt.show()
cv2.destroyAllWindows()