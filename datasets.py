from PIL import Image, ImageDraw, ImageFont
import os
import math
import uuid
import numpy as np
from enum import Enum, auto

size = 400
s = 224
dirName = './data/'
radius = 140
numRandom = 15000
numRandom = 2000
ballSize = 45
ballXloc = 200 - ballSize/2
ballYloc = 182 - ballSize/2
ballSize = 25
ballXloc = 200 - ballSize/2
ballYloc = 182 - ballSize/2
rectXloc = 180
rectYloc = 162
rectSize = 40


class C(Enum):
    white = 0
    red = 1
    blue = 2
    green = 3
    yellow = 4
    black = 5


class Shape(Enum):
    circle = auto()
    square = auto()
    star = auto()
    random = auto()


allColors = [(255, 255, 255), (220, 0, 0), (65, 105, 225), (50, 205, 50), (252, 227, 7), (0, 0, 0)]
stageRange = [[5, 6], [5, 6], [5, 6], [6, 14], [7, 14]]
stageNumColors = [2, 2, 5, 5, 5]

stage8BallsNum = [[7, 4, 2], [7, 4, 2], [6, 4, 3], [6, 4, 3], [6, 4, 3], [7, 4, 2]]
stage8Dom = [0, 2, 2, 0, 1, 1]
stage8Class = [1, 0, 0, 1, 0, 0]


def makeDir(dir):
    dir = dirName + dir
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(dir + '0/'):
        os.mkdir(dir + '0/')
    if not os.path.exists(dir + '1/'):
        os.mkdir(dir + '1/')


def saveImage(image, dir, m):
    image = image.resize((s, s))
    r = uuid.uuid1().hex[0:14]
    if m:
        r = '1/' + r
    else:
        r = '0/' + r
    image.save(dirName + dir + r + '.png')


def drawRing(draw, c):
    draw.ellipse((20, 2, 380, 362), fill=c)
    draw.ellipse((30, 12, 370, 352), fill=allColors[C.black.value])
    return draw


def drawImage(imgName, ring, balls, shape=Shape.circle):
    image = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(image)
    drawRing(draw, allColors[ring.value])
    angle = 360.0 / float(len(balls))
    for i in range(len(balls)):
        newShape = shape
        if shape==Shape.random:
            newShape = np.random.choice([shape.circle, shape.square, shape.star])
        if newShape==Shape.circle:
            x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
            y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
            draw.ellipse((x, y, x + ballSize, y + ballSize), fill=allColors[balls[i].value])
        elif newShape==Shape.square:
            x = rectXloc + radius * math.sin(i * angle * math.pi / 180.0)
            y = rectYloc - radius * math.cos(i * angle * math.pi / 180.0)
            draw.rectangle((x, y, x + rectSize, y + rectSize), fill=allColors[balls[i].value])
        elif newShape==Shape.star:
            x = rectXloc + radius * math.sin(i * angle * math.pi / 180.0)
            y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
            draw.text((x, y), '*', allColors[balls[i].value], ImageFont.truetype('arial.ttf', 100))
    image.resize((s, s))
    image.save('./' + imgName + '.png')


def createStage1():
    dir = 'Stage1/'
    makeDir(dir)
    colors = [C.white, C.red]
    angle = 360.0 / 5.0
    for rc in colors:
        image = Image.new('RGB', (size, size))
        draw = ImageDraw.Draw(image)
        draw = drawRing(draw, rc)
        for j, c in enumerate(colors):
            for i in range(-1, 2):
                x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                draw.ellipse((x, y, x + ballSize, y + ballSize), fill=allColors[c.value])
            for i in range(2, 4):
                x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                draw.ellipse((x, y, x + ballSize, y + ballSize), fill=allColors[colors[j - 1].value])
            saveImage(image, dir, rc == c)


def createStage2to4(stage, ordered=True):
    dir = 'Stage' + str(stage) + '/'
    makeDir(dir)
    stage = stage - 1
    for c1 in range(stageNumColors[stage] - 1):
        for c2 in range(c1 + 1, stageNumColors[stage]):
            colors = [allColors[c1], allColors[c2]]
            for t in range(stageRange[stage][0], stageRange[stage][1]):
                angle = 360.0 / float(t)
                for rc in colors:
                    for m in range(2):
                        o = 1 if ordered else math.floor(t / 2)
                        for j in range(o):
                            a = np.ones(t).astype(np.int8) * m
                            a[0] = -m + 1
                            a[j + 1] = a[0]
                            for l in range(t):
                                a = np.roll(a, 1)
                                image = Image.new('RGB', (size, size))
                                draw = ImageDraw.Draw(image)
                                draw = drawRing(draw, rc)
                                for i in range(t):
                                    x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                    y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                    draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[a[i]])
                                #if np.random.random()< 0.27:
                                saveImage(image, dir, rc == colors[m])


def createStage5(ordered):
    dir = 'Stage5/'
    makeDir(dir)
    if ordered:
        for c1 in range(4):
            for c2 in range(c1 + 1, 5):
                colors = [allColors[c1], allColors[c2]]
                for t in range(7, 14):
                    angle = 360.0 / float(t)
                    for m in range(3, math.floor((t - 1) / 2) + 1):
                        for r in range(t):
                            for rc in colors:
                                image = Image.new('RGB', (size, size))
                                draw = ImageDraw.Draw(image)
                                draw = drawRing(draw, rc)
                                for j, c in enumerate(colors):
                                    for i in range(r, t + r - m):
                                        x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                        y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                        draw.ellipse((x, y, x + ballSize, y + ballSize), fill=c)
                                    for i in range(t + r - m, t + r):
                                        x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                        y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                        draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[j - 1])
                                    saveImage(image, dir, rc == c)
    else:
        for j in range(numRandom):
            t = np.random.randint(11, 14)
            angle = 360.0 / float(t)
            least = np.random.randint(3, math.floor((t - 1) / 2) + 1)
            c1 = np.random.randint(0, 5)
            c2 = c1
            while c2 == c1:
                c2 = np.random.randint(0, 5)
            dom = np.random.choice([c1, c2], 1)[0]
            a = np.ones(t).astype(np.int8) * c1
            for i in range(least):
                a[i] = c2
            np.random.shuffle(a)
            image = Image.new('RGB', (size, size))
            draw = ImageDraw.Draw(image)
            draw = drawRing(draw, allColors[dom])
            for i in range(t):
                x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                draw.ellipse((x, y, x + ballSize, y + ballSize), fill=allColors[a[i]])
            saveImage(image, dir, dom == c1)


def createStage5Extended(ordered):
    dir = 'Stage5/'
    if ordered:
            for c1 in range(4):
                for c2 in range(c1 + 1, 5):
                    colors = [allColors[c1], allColors[c2]]
                    for t in range(30, 31):
                        angle = 360.0 / float(t)
                        for m in range(3, math.floor((t - 1) / 2) + 1):
                            for r in range(t):
                                for rc in colors:
                                    image = Image.new('RGB', (size, size))
                                    draw = ImageDraw.Draw(image)
                                    draw = drawRing(draw, rc)
                                    for j, c in enumerate(colors):
                                        if rc == c:
                                            nc = t - m
                                        else:
                                            nc = m
                                        makeDir(dir+str(nc)+'/')
                                        for i in range(r, r + t - m):
                                            x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                            y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                            draw.ellipse((x, y, x + ballSize, y + ballSize), fill=c)
                                        for i in range(r + t - m, r + t):
                                            x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                            y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                            draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[j - 1])
                                        saveImage(image, dir+str(nc)+'/', rc == c)


def createStage6(ordered):
    dir = 'Stage6/'
    makeDir(dir)
    if ordered:
        for c1 in range(5):
            for c2 in range(5):
                if c1 == c2:
                    continue
                for c3 in range(5):
                    if c3 == c1 or c3 == c2:
                        continue
                    colors = [allColors[c1], allColors[c2], allColors[c3]]
                    for t in range(11, 14):
                        angle = 360.0 / float(t)
                        for r in range(t):
                            for rc in colors:
                                if rc == colors[1]:  # mid can not match
                                    continue
                                image = Image.new('RGB', (size, size))
                                draw = ImageDraw.Draw(image)
                                draw = drawRing(draw, rc)
                                for j, c in enumerate(colors):
                                    for i in range(r, t + r - 5):
                                        x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                        y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                        draw.ellipse((x, y, x + ballSize, y + ballSize), fill=c)
                                    for i in range(t + r - 5, t + r - 2):
                                        x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                        y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                        draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[j - 1])
                                    for i in range(t + r - 2, t + r):
                                        x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                        y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                        draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[j - 2])
                                    saveImage(image, dir, rc == c)
    else:
        for j in range(numRandom):
            t = np.random.randint(11, 14)
            angle = 360.0 / float(t)
            least = 2
            mid = 3
            c1 = np.random.randint(0, 5)
            c2 = c1
            while c2 == c1:
                c2 = np.random.randint(0, 5)
            c3 = c1
            while c3 == c1 or c3 == c2:
                c3 = np.random.randint(0, 5)
            dom = np.random.choice([c1, c3], 1)[0]
            a = np.ones(t).astype(np.int8) * c1
            for i in range(mid):
                a[i] = c2
            for i in range(mid, mid + least):
                a[i] = c3
            np.random.shuffle(a)
            image = Image.new('RGB', (size, size))
            draw = ImageDraw.Draw(image)
            draw = drawRing(draw, allColors[dom])
            for i in range(t):
                x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                draw.ellipse((x, y, x + ballSize, y + ballSize), fill=allColors[a[i]])
            saveImage(image, dir, dom == c1)


def createStage8(ordered):
    angle = 360.0 / 13.0
    for stage in range(6):
        dir = 'Stage8.' + str(s + 1) + '/'
        makeDir(dir)
        if ordered:
            for c1 in range(5):
                for c2 in range(5):
                    if c1 == c2:
                        continue
                    for c3 in range(5):
                        if c3 == c1 or c3 == c2:
                            continue
                        colors = [allColors[c1], allColors[c2], allColors[c3]]
                        for j in range(2):
                            for r in range(13):
                                image = Image.new('RGB', (size, size))
                                draw = ImageDraw.Draw(image)
                                dom = stage8Dom[stage] if stage8Dom[stage] == 0 or j == 0 else 3 - stage8Dom[stage]
                                draw = drawRing(draw, colors[dom])
                                for i in range(r, r + stage8BallsNum[stage][0]):
                                    x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                    y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                    draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[0])
                                for i in range(r + stage8BallsNum[stage][0],
                                               r + stage8BallsNum[stage][0] + stage8BallsNum[stage][1 + j]):
                                    x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                    y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                    draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[1])
                                for i in range(r + stage8BallsNum[stage][0] + stage8BallsNum[stage][1 + j],
                                               r + stage8BallsNum[stage][0] + stage8BallsNum[stage][1] +
                                               stage8BallsNum[stage][2]):
                                    x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                                    y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                                    draw.ellipse((x, y, x + ballSize, y + ballSize), fill=colors[2])
                                saveImage(image, dir, stage8Class[stage])
        else:
            for j in range(numRandom):
                c1 = np.random.randint(0, 5)
                c2 = c1
                while c2 == c1:
                    c2 = np.random.randint(0, 5)
                c3 = c1
                while c3 == c1 or c3 == c2:
                    c3 = np.random.randint(0, 5)
                colors = [allColors[c1], allColors[c2], allColors[c3]]
                a = np.ones(13).astype(np.int8) * c1
                for i in range(stage8BallsNum[stage][1]):
                    a[i] = c2
                for i in range(stage8BallsNum[stage][1], stage8BallsNum[stage][1] + stage8BallsNum[stage][2]):
                    a[i] = c3
                np.random.shuffle(a)
                image = Image.new('RGB', (size, size))
                draw = ImageDraw.Draw(image)
                draw = drawRing(draw, colors[stage8Dom[stage]])
                for i in range(13):
                    x = ballXloc + radius * math.sin(i * angle * math.pi / 180.0)
                    y = ballYloc - radius * math.cos(i * angle * math.pi / 180.0)
                    draw.ellipse((x, y, x + ballSize, y + ballSize), fill=allColors[a[i]])
                saveImage(image, dir, stage8Class[stage])


def main():
    # createStage1()
    #createStage2to4(2, ordered=False)
    #createStage2to4(3, ordered=False)
    #createStage2to4(4, ordered=False)
    #createStage5(ordered=False)
    createStage5Extended(ordered=True)
    # createStage6(ordered=False)
    # createStage8(ordered=False)
    '''drawImage('30.1', C.yellow, [C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.white, C.white, C.white, C.white, C.white], Shape.circle)'''
    '''drawImage('17.4', C.yellow, [C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.white,C.white, C.white, C.white, C.white,
                                 C.green,C.green, C.green,
                                 C.red, C.red], Shape.circle)
    drawImage('17.5A', C.white, [C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.white,C.white, C.white, C.white, C.white,
                                 C.green,C.green, C.green,
                                 C.red, C.red], Shape.circle)
    drawImage('17.5B', C.green, [C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.white,C.white, C.white, C.white, C.white,
                                 C.green,C.green, C.green,
                                 C.red, C.red], Shape.circle)
    drawImage('17.6A', C.white, [C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.white,C.white, C.white,
                                 C.green,C.green, C.green,
                                 C.red, C.red], Shape.circle)
    drawImage('17.6B', C.green, [C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow, C.yellow,
                                 C.white,C.white, C.white,
                                 C.green,C.green, C.green,
                                 C.red, C.red], Shape.circle)'''
    '''drawImage('s2A', C.red, [C.white,C.white, C.white, C.white,C.white, C.white,
                              C.red, C.red, C.red, C.red,
                              C.blue, C.blue, C.blue], Shape.circle)'''


if __name__ == '__main__':
    main()
