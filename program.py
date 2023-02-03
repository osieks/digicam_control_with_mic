
import speech_recognition as sr
import time
import playsound as ps
import pyautogui

debug = 0

def main():
   # this is called from the background thread
    def callback(recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            text =recognizer.recognize_google(audio,language="pl")
            text =  " " + text
            print("You said: " + text)
            #if("Jan" in text or " 0" in text or "Janie" in text or "zero" in text):
            if("zdjęcie" in text):
                robienie_zdjecia_odliczanie()
            if("focus" in text or "fokus" in text or "Focus" in text or "Fokus" in text):
                lokalizuj_i_kliknij("przycisk_focus.png")
                ps.playsound("fokus.mp3")

        except sr.UnknownValueError:
            print("Could not understand audio.")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    m = sr.Microphone()
    r = sr.Recognizer()
    #r.energy_threshold=600
    r.pause_threshold= 0
    r.non_speaking_duration=0

    with m as source:
        print("listening to ambient")
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        print("end of listening to ambient")

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    print("odpalenie listening in background")
    stop_listening = r.listen_in_background(m, callback)
    print("listening in the background")
    ps.playsound("gotowy.mp3")

    # infinite loop for program to run in the background
    while True: time.sleep(0.1)

def robienie_zdjecia_odliczanie():
    ps.playsound("3.mp3")
    time.sleep(0.6)
    ps.playsound("2.mp3")
    time.sleep(0.6)
    ps.playsound("1.mp3")
    if 'time_taking_photo' in locals():
        time.sleep(0.6-time_taking_photo)
    else:
        time.sleep(0)
    start_time = time.time()
    lokalizuj_i_kliknij("przycisk_zdjecie.png")
    end_time = time.time()
    time_taking_photo=end_time - start_time
    if time_taking_photo<=0:
        time_taking_photo=0
    print(time_taking_photo)
    ps.playsound("0.mp3")

def lokalizuj_i_kliknij(filename):    
    found = 0
    conf = 1
    conf_step = 0.05

    while found==0:
            if conf<0.85:
                print("nie znalazłem przycisku na ekranie")
                ps.playsound("zasloniete.mp3")
                break

            if debug==1:
                print('conf'+str(conf))
            red_location = pyautogui.locateCenterOnScreen(filename,confidence=conf)
            
            if debug==1:
                print(red_location)
           
            if(red_location != None):
                if debug==1:
                    print('found')
                    pyautogui.moveTo(red_location)
                else:
                    pyautogui.click(red_location)
                found = 1
            
            else:
                if debug==1:
                    print("conf "+str(conf))
                conf=conf-conf_step
                if conf<conf_step:
                    conf=1

if __name__ == "__main__":
    main()