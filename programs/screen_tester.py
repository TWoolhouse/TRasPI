from gfxhat import lcd
from random import randint

for i in range(0,100):
    lcd.set_pixel((randint(0,128)),(randint(0,64)),1)
    lcd.show()
