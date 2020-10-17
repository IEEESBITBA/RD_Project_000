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
error = False
while True:
    cv2.imshow('Canvas',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(20) & 0xFF == ord('c'):
        img = cv2.medianBlur(img, 3)
        chars_img = []
        chars_txt = []
        temp = []
        char_heights = []
        centers = []
        char_centers = []
        heights = []
        subscripts = []
        superscripts = []
        aux = []
        boxes = tess.image_to_boxes(img, lang="eng+equ")
        h, w, _ = img.shape
        if boxes:
            for b in boxes.splitlines():
                b = b.split(' ')
                aux.append(b)
                temp = np.copy(img[h-(int(b[4])):h-(int(b[2])), int(b[1]):int(b[3])])
                chars_img.append(temp)
                chars_txt.append(b[0])
                img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
                centers.append([(int(b[3])+int(b[1]))/2, ((h-int(b[4])) + (h-int(b[2])))/2])
            print(chars_txt)
        else:
            print("nothing found")
            error = True
        while True:
            cv2.imshow('Canvas', img)
            i=0
            for char in chars_img:
                i = i+1
                cv2.imshow("Character" + str(i), char)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        if error is not True:
            for point in centers:
                heights.append(point[1])
            mean_height = np.mean(heights) #calculo media y desvio
            std_height = np.std(heights)
            if(std_height > 5):
                for point in centers:
                    if (point[1] < mean_height + std_height) and (point[1] > mean_height - std_height):
                        char_centers.append(point)
                for point in char_centers:
                    char_heights.append(point[1])
                mean_char_height = np.mean(char_heights)
                std_char_height = np.std(char_heights)
                for i in range(len(centers)):
                    if centers[i][1]  > mean_char_height + 2*std_char_height:
                        subscripts.append(aux[i][0])
                    elif centers[i][1] < mean_char_height - 2*std_char_height:
                        superscripts.append(aux[i][0])

            print("possible superscript characters: ")
            print(superscripts)
            print("possible subscript characters: ")
            print(subscripts)

    #elif cv2.waitKey(20) & 0xFF == ord('s'):
    #    img = cv2.resize(img, (50, 50))
    #    FileHandling.saveImage(img)
    #    break

plt.show()
cv2.destroyAllWindows()