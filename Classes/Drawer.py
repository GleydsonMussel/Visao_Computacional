import cv2

class Drawer:
    
    @staticmethod
    def draw_roi(frame, x, w, y, h, cx, cy):
        cv2.rectangle(frame,(x, y), (x+w, y+h), (255,0,0),2)
        Drawer.draw_center(frame, cx, cy)

    @staticmethod
    def draw_center(frame, cx, cy):
        cv2.circle(frame, (cx,cy), 5, (0,0,255),-1)
    
    @staticmethod    
    def write_on_video(frame, texto, posicao, cor, tamanho = 1, grossura = 2):
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        cv2.VideoWriter()
        cv2.putText(frame, texto,posicao, fonte, tamanho, cor, grossura)