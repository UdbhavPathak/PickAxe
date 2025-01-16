from PIL import Image
size = [2176//16,238]
#32,28,59
#22,23,37
def changecolor(img,path):
    img = img.convert("RGBA")
    data = img.getdata()
    new = []
    for items in data:
        new.append((items[2],items[1],items[0],items[3]))

    img.putdata(new)
    img.save(path)

def removebg(img,path):
    img = img.convert("RGBA")
    data = img.getdata()
    new = []
    for items in data:
        if items[0] <= 32 and items[1] <= 28 and items[2] <= 59 :
            new.append((0,0,0,0))
        else:
            new.append(items)
    img.putdata(new)
    img.save(path)



# for i in range(0,5):
#     img = Image.open("images/recycle/idlesheet.png")
#     img2 = img.crop((size[0]*i,0,size[0]*(i+1),size[1]))
#     img2.save(f"images/idle2/{i+1}.png")
#
# for i in range(1,6):
#     img = Image.open(f"images/idle2/{i}.png")
#     changecolor(img,f"images/idle2/{i}.png")
#     img = Image.open(f"images/idle2/{i}.png")
#     removebg(img,f"images/idle2/{i}.png")
# size = (700//4,100)
# n = 0
# for y in range(0,2):
#     for x in range(0,4):
#         img = Image.open("images/torch.png")
#         img2 = img.crop((size[0]*x,y*size[1],size[0]*(x+1),size[1]*(y+1)))
#         img2.save(f"images/torch/{n}.png")
#         n += 1

#14812,708
width = 14812//28
height = 708
img = Image.open("images/killer.png")
changecolor(img,"images/killer2.png")