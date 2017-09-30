from PIL import Image
import subprocess

def cleanFile(filePath,newFilePath):
    image = Image.open(filePath)
    image = image.point(lambda x: 0 if x<143 else 255)
    image.save(newFilePath)

    subprocess.call(["tesseract",newFilePath,"mjorcen.normal.exp0","-l","normal"])
    outputFile = open("output.txt",'rb')
    print(outputFile.read().decode('utf-8'))
    outputFile.close()
cleanFile("mjorcen.normal.exp0.png","test6.png")