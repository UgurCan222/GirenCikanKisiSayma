#      JGPGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGPPY  
#      YBB?77!!!!!!!!!!!!!!!!!!777!!!!!!!!!!!!77?BB5  
#      YBG. :!!!!!!!!!!!!!!!!!!  ^!!!!!!!!!!!!^ :GB5  
#      YBG: ?#BBBBBBBBBBBBBBBBG. J#BBBBBBBBBB#J :GB5  
#      YBG: ?BBBBBBBBBBBBBBBBBG. JBBBBBBBBBBBBJ :GB5  
#      YBG: ?BBBBBBGPPPPPPPPBBG. JBBBBBBBBBBBBJ :GB5  
#      YBG: ?BBBBBBY       .GBG. JBBBBBBBBBBBBJ :GB5  
#      YBG: ?BBBBBBJ       .GBG. J#BBBBBBBBBB#J :GB5  
#      YBG: ?BBBBBBJ       .GBG. !JJJJJJJJJJJJ! :GB5  
#      YBG: ?BBBBBB5^^^^^^^~GBG!^^^^^^^^^^^^^^: :GB5  
#      YBG: 7BGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBJ :GB5  
#      YBG: .::::::::::::::^GBG^:::::::YBBBBBBJ .GB5  
#      YBG: !5YYYYYYYYYY57 .PBG.       JBBBBBBJ .GB5  
#      YBG: ?#BBBBBBBBBB#Y .PBG.       JBBBBBBJ .GB5  
#      YBG: ?BBBBBBBBBBBBY .PBG:.......JBBBBBBJ .GB5  
#      YBG: ?BBBBBBBBBBBBY .PBBGGGGGGGGGBBBBBBJ .GB5  
#      YBG: ?BBBBBBBBBBBBY .PBBBBBBBBBBBBBBBBBJ .GB5  
#      YBG: ?#BBBBBBBBBB#Y .GBBBBBBBBBBBBBBBB#J .GB5  
#      YBG. :~~~~~~~~~~~~:  ^~~~~~~~~~~~~~~~~~: .GB5  
#      YBBJJJ?????????????JJ???????????????????JJBB5  
#      ?5555555555555555555555555555555555555555555? 

#       FIRAT ÜNİVERSİTESİ BİLGİSAYAR MÜHENDİSLİĞİ
#       195260063 UĞUR CAN









import cv2          #Görüntü işleme için OpenCV kütüphanesini import ediyorum.



Kayit = cv2.VideoCapture('C:/Users/ugurc/Desktop/deneme.mp4')
Bos_goruntu = cv2.imread('C:/Users/ugurc/Desktop/deneme_bos.jpeg')

contour_eski = [] # contour_guncel listesini de ileriki aşamalara çektim. Detayları o kısımda.
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG() #Bu kod, OpenCV'nin MOG (Mixture of Gaussians) arka plan çıkarıcısı nesnesini oluşturur.
fgmask = fgbg.apply(Bos_goruntu)
sayac = 0
Girenler,Cikanlar = 0,0

while(Kayit.isOpened()):
            
        oynatici, frame = Kayit.read()   
        Cizgi = frame.shape[0] * 253 // 480
        fgmask = fgbg.apply(frame) 
        #  (foreground mask): Arka plan çıkarımı (background subtraction) algoritması kullanılarak,önceki karelerden farklı olarak, ön planda yer alan objeleri gösteren binary maske.
        
        thresh = cv2.dilate(fgmask, None, iterations=1)   
        #  Binary eşikleme (thresholding) işlemi uygulanarak, fgmask üzerindeki gürültüleri kaldırmak ve daha net konturlar elde etmek için kullanılan maske.               
        
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]   
        #  thresh maskesi üzerindeki nesnelerin kontürlerini (outline) temsil eden Koordinatların listesi.
        
        contour_guncel = [] #  Bu satırda, contour_guncel listesi her kare için güncellenen bir liste olduğu için, her döngüde başlangıçta boş bir liste olarak tanımlanır.
                #  Bu, daha önceki karelerdeki konturları tutan contour_eski listesinden ayrı tutulur.
                #  Sonraki döngüde, contour_guncel listesi güncellendiğinde, önceki karelerdeki konturları saklamak için ayrılan contour_eski listesi,
                #  mevcut contour_guncel listesine eşitlenir ve böylece sonraki kare için önceki konturlar saklanır.
        
     
#-------------------------------------------------------------------------------
        for c in cnts:
                
            if cv2.contourArea(c) < 800:
                continue
             
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  
            
            contour_guncel.append([x,y])
        
        
        if ( len(contour_eski) == 0 or len(contour_guncel) == 0 ): 
            contour_eski = contour_guncel 
            continue
 #  Bu döngüde, cv2.findContours fonksiyonu tarafından bulunan tüm konturları döngüye sokar.
 #  Konturun alanı 800'den küçükse, yani yetersiz bir alana sahipse döngüyü atlar ve bir sonraki kontura geçer.
 #  Daha sonra, konturun etrafına bir dikdörtgen çizilir ve bu dikdörtgenin sol üst köşesi (x,y) ve sağ alt köşesi (x+w,y+h) olarak kaydedilir.
 #  Son olarak, contour_guncel listesine dikdörtgenin sol üst köşesinin koordinatları eklenir. Eğer contour_eski listesi boş ise veya contour_guncel listesi boş ise,
 #  contour_eski listesi contour_guncel listesi ile değiştirilir ve döngü devam eder.
 #------------------------------------------------------------------------------       


        en_yakin_contour_listesi = [] 

        for i in range ( len(contour_guncel) ):
            
            minimum = 10000000 #bu değeri videoya göre deneme yanılma yoluyla yazdım, değiştirebilirsiniz.
# Eğer 69. satırdaki "if cv2.contourArea(c) < 800:" koşulu doğruysa, yani kontur alanı 800'den küçükse, o zaman bu konturu çıkarırız ve bu nedenle minimum alan 
# değerini güncellemek için 93. satırdaki "minimum = 10000000" ifadesine gerek yoktur. Ancak, 69. satırdaki koşul yanlışsa, yani kontur alanı 800 veya daha büyükse,
# o zaman minimum alan değerini belirlemek için 93. satırdaki "minimum = 10000000" ifadesi gereklidir. Bu nedenle, minimum alan değeri hesaplanmadan önce kontur 
# alanının koşulu karşılayıp karşılamadığını kontrol etmek önemlidir.               
            for k in range ( len(contour_eski) ):
                
                fark_x = contour_guncel[i][0] - contour_eski[k][0]
                fark_y = contour_guncel[i][1] - contour_eski[k][1]
                
                mesafe = fark_x * fark_x + fark_y * fark_y
                
                if ( mesafe < minimum ):
                    minimum =  mesafe
                    enyakincontour = k
                    
            en_yakin_contour_listesi.append(enyakincontour)
            
         
        for i in range ( len(contour_guncel) ):
            
            y_onceki = contour_eski[en_yakin_contour_listesi[i]][1]
 
            if ( contour_guncel[i][1] < Cizgi and y_onceki > Cizgi ):
                Cikanlar = Cikanlar + 1 
        
            if ( contour_guncel[i][1] > Cizgi and y_onceki < Cizgi ):
                Girenler = Girenler + 1 
        
        contour_eski = contour_guncel     

#  Mantık Şu şekildedir : Hareket yönleri, önceki ve güncel konturlar arasındaki farkların hesaplanması yoluyla belirleniyor. 
# İlk olarak, güncel karedeki tüm konturlar, belirli bir alan eşiği kullanılarak sınırlayıcı çerçevelere dönüştürülüyor. 
# Daha sonra, önceki ve güncel karedeki kontur listeleri arasında eşleşme sağlamak için, her bir güncel konturun önceki karedeki hangi kontura en yakın 
# olduğu hesaplanıyor.
# Bu hesaplama, öklid mesafesi kullanarak yapılmaktadır. Konturların önceki ve güncel karelerdeki konumları arasındaki mesafe hesaplanarak, 
# en yakın önceki kontur belirlenir. Daha sonra, her bir güncel konturun önceki karedeki hangi kontura en yakın olduğu bilgisi, bir liste olarak saklanır.
# Bu listeyi kullanarak, her bir güncel konturun hareket yönü belirlenir. Eğer kontur çizginin altındaysa, o zaman nesne "çıktı" olarak kabul edilir 
# ve Cikanlar değişkeni artırılır. Eğer kontur çizginin üstündeyse, nesne "girdi" olarak kabul edilir ve Girenler değişkeni artırılır.


#  İlk önce en_yakin_contour_listesi adında bir boş liste tanımlanır. Daha sonra, contour_guncel ve contour_eski adında iki farklı kontur listesi var. 
#  Bu listeler, her karede tespit edilen kontur noktalarını içerir.
#  en_yakin_contour_listesi, contour_guncel ve contour_eski listeleri arasındaki minimum mesafeye sahip kontur noktalarının indekslerini içerir.
#  Bu işlem, her bir konturun önceki karedeki kontura en yakın olanı olduğunu belirlemek için yapılır.
#  Daha sonra, contour_guncel listesi içindeki kontur noktalarının yönü, önceki karedeki konturların yönü ile karşılaştırılır.
#  Kontur noktaları, belirli bir çizginin altında mı yoksa üstünde mi olduğuna göre sayıları arttırılır. 
#  Son olarak, contour_eski listesi, contour_guncel listesi ile değiştirilir ve işlem bir sonraki karede tekrarlanır.


 #------------------------------------------------------------------------------                
        
        cv2.line(frame,(0,Cizgi),(frame.shape[1],Cizgi),(0,255,255),3) 
        #  cv2.line() fonksiyonu, ilk olarak frame adlı görüntü üzerinde çalıştığını belirtmektedir.
        #  İkinci parametre olarak çizginin başlangıç koordinatlarını belirtirken, (0, Cizgi) koordinatları verilmiştir.
        #  Burada Cizgi değişkeni, çizgiyi yukarıdan aşağıya doğru geçirecek olan y eksenindeki piksel konumunu temsil ediyor.
        #  Üçüncü parametre ise çizginin bitiş koordinatlarını belirtirken, frame.shape[1] değişkeni, görüntünün genişliğini temsil etmektedir.
        #  Dördüncü parametre olarak seçilen (0, 255, 255) rengi ise çizginin sarı renkte olmasını sağlayacaktır.
        #  Son olarak, çizginin kalınlığını belirlemek için 3 değeri verilmiştir.
        
        cv2.putText(frame, "Giren: " + str(Girenler) ,(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)           
        cv2.putText(frame, "Cikan: " + str(Cikanlar) ,(10,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
     
        
        
        cv2.imshow('Kamera',frame)  #  Kamera adlı bir pencere açıp yapılanları izleyelim.
        cv2.imshow('Arkaplan Cikartmasi',fgmask)  #  Bu satırı yöntem görülsün diye ekledim, kullanıcılar bu satırı kaldırabilirler.
        
    
        k = cv2.waitKey(30) #  Kareler arasındaki geçiş süresi 30 milisaniye olarak alındı.
        if k == 27:  #  ESC tuşu ile çıkış yapılır.
            break


Kayit.release()
cv2.destroyAllWindows()