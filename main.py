# Saya [Muhammad Satria Ramadhani - 2005128] mengerjakan evaluasi [Tugas
# Praktikum 03] dalam mata kuliah [Desain dan Pemrograman Berorientasi Objek]
# untuk keberkahan-Nya, maka saya tidak melakukan kecurangan seperti yang
# telah dispesifikasikan. Aamiin.

# Import library.
from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter.ttk import Combobox
import mysql.connector

# Prepare MySQL connection and create its cursor.
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "dpbo_tp3")
dbcursor = mydb.cursor()

# Create root element.
root = Tk()
root.title("Tugas Praktikum 03 - DPBO")

img_index = 0
img_name = ["bigdata.png", "labprak.png", "microteaching.png", "rpl.png", "tkj.png"]
img_view = []

for i in img_name:
    img_view.append(ImageTk.PhotoImage(PIL.Image.open("Image/Facilities/" + i)))

# Get data.
def getMhs():
    # Use MySQL connection.
    global mydb
    global dbcursor

    # Execute SELECT query and get all row.
    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    # Return all row as a result. 
    return result

# Insert data.
def insertData(parent, nama, nim, jk, jurusan, hobi):
    # Create top-level window.
    top = Toplevel()
    
    # Get data based on available form.
    nim = nim.get(); nama = nama.get(); jurusan = jurusan.get()
    jk = jk.get(); hobi = hobi.get()

    # Check if there is no empty data.
    if ((nim) and (nama) and (jk) and (jurusan) and (hobi)):
        # Prepare and execute query.
        query = "INSERT INTO mahasiswa VALUES ('', %s, %s, %s, %s, %s)"
        value = (nim, nama, jk, jurusan, hobi)
        dbcursor.execute(query, value)
        mydb.commit()

        # Confirmation.
        label = Label(top, text = "Data berhasil diinput bosque!").grid(row = 0, column = 0, sticky = "w")
        btn_ok = Button(top, text = "Syap!", anchor = "s", command = lambda:[top.destroy(), parent.deiconify()])
        btn_ok.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")
    
    else:
        # Give an error if there is empty data.
        label = Label(top, text = "Data masih ada yang kosong!").grid(row = 0, column = 0, sticky = "w")
        btn_ok = Button(top, text = "Syap!", anchor = "s", command = lambda:[top.destroy(), parent.deiconify()])
        btn_ok.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")

# Delete all data.
def delAll():
    # Create top level for confirmation dialog.
    top = Toplevel()

    # There are two methods to delete all data from a table (DELETE and TRUNCATE).
    # However, I'd prefer TRUNCATE method because it'll reset AUTO_INCREMENT
    # attribute to 0 / 1.
    
    # Execute TRUNCATE query and apply it to database.
    dbcursor.execute("TRUNCATE mahasiswa")
    mydb.commit()

    # Confirmation.
    label = Label(top, text = "Data berhasil dihapus!").pack(pady = 20)
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

# Window of input data.
def inputs():
    # Hide root window.
    global root
    root.withdraw()

    # INPUT FORM. #

    # Create top-level window and its frame.
    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text = "Input Data Mahasiswa", padx = 10, pady = 10)
    dframe.pack(padx = 10, pady = 10)
    
    # Input 1 (Name).
    label1 = Label(dframe, text = "Nama Mahasiswa").grid(row = 0, column = 0, sticky = "w")
    input_nama = Entry(dframe, width = 30)
    input_nama.grid(row = 0, column = 1, padx = 20, pady = 10, sticky = "w")
    
    # Input 2 (NIM / Student ID).
    label2 = Label(dframe, text = "NIM").grid(row = 1, column = 0, sticky = "w")
    input_nim = Entry(dframe, width = 30)
    input_nim.grid(row = 1, column = 1, padx = 20, pady = 10, sticky = "w")
    
    # Input 3 (Gender).
    label3 = Label(dframe, text = "Jenis Kelamin").grid(row = 2, column = 0, sticky = "w")
    input_jk = StringVar(dframe, "Laki-laki")
    input3_0 = Radiobutton(dframe, text = "Laki-laki", variable = input_jk, value = "Laki-laki")
    input3_0.grid(row = 2, column = 1, padx = 20, pady = 10, sticky = 'w')
    input3_1 = Radiobutton(dframe, text = "Perempuan", variable = input_jk, value = "Perempuan")
    input3_1.grid(row = 2, column = 2, padx = 20, pady = 10, sticky = 'w')

    # Input 4 (Study Program).
    label4 = Label(dframe, text = "Jurusan").grid(row = 3, column = 0, sticky = "w")
    options_jurusan = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(dframe)
    input_jurusan.set(options_jurusan[0])
    input4 = OptionMenu(dframe, input_jurusan, *options_jurusan)
    input4.grid(row = 3, column = 1, padx = 20, pady = 10, sticky = 'w')

    # Input 5 (Hobby).
    input_hobi = StringVar(dframe)
    label5 = Label(dframe, text = "Hobi").grid(row = 4, column = 0, sticky = "w")
    input5 = Combobox(dframe, textvariable = input_hobi)
    input5['values'] = ("Bermain Game", "Bernyanyi", "Jalan-jalan", "Menulis")
    input5.grid(row = 4, column = 1, padx = 20, pady = 10, sticky = 'w')

    # Cretae button frame.
    frame2 = LabelFrame(dframe, borderwidth = 0)
    frame2.grid(columnspan = 2, column = 0, row = 10, pady = 10)

    # Submit Button
    btn_submit = Button(frame2, text = "Submit Data", anchor = "s", command = lambda:[insertData(top, input_nama, input_nim, input_jk, input_jurusan, input_hobi), top.withdraw()])
    btn_submit.grid(row = 3, column = 0, padx = 10)

    # Cancel Button
    btn_cancel = Button(frame2, text = "Gak jadi / Kembali", anchor = "s", command = lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row = 3, column = 1, padx = 10)

# Window of show all data.
def viewAll():
    # Hide root window.
    global root
    root.withdraw()

    # Create top-level window and its frame.
    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth = 0)
    frame.pack()

    # Cancel button.
    btn_cancel = Button(frame, text = "Kembali", anchor = "w", command = lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
    
    # Head title.
    head = Label(frame, text = "Data Mahasiswa")
    head.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "w")

    # Create table frame.
    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get all data from database.
    result = getMhs()

    # Table title / heading.
    title1 = Label(tableFrame, text = "No.", borderwidth = 1, relief = "solid", width = 3, padx = 5).grid(row = 0, column = 0)
    title2 = Label(tableFrame, text = "NIM", borderwidth = 1, relief = "solid", width = 15, padx = 5).grid(row = 0, column = 1)
    title3 = Label(tableFrame, text = "Nama", borderwidth = 1, relief = "solid", width = 20, padx = 5).grid(row = 0, column = 2)
    title4 = Label(tableFrame, text = "Jenis Kelamin", borderwidth = 1, relief = "solid", width = 20, padx = 5).grid(row = 0, column = 3)
    title5 = Label(tableFrame, text = "Jurusan", borderwidth = 1, relief = "solid", width = 20, padx = 5).grid(row = 0, column = 4)

    # Table 
    i = 0
    for data in result:
        label1 = Label(tableFrame, text = str(i+1), borderwidth = 1, relief = "solid", height = 2, width = 3, padx = 5).grid(row = i+1, column = 0)
        label2 = Label(tableFrame, text = data[1], borderwidth = 1, relief = "solid", height = 2, width = 15, padx = 5).grid(row = i+1, column = 1)
        label3 = Label(tableFrame, text = data[2], borderwidth = 1, relief = "solid", height = 2, width = 20, padx = 5).grid(row = i+1, column = 2)
        label4 = Label(tableFrame, text = data[3], borderwidth = 1, relief = "solid", height = 2, width = 20, padx = 5).grid(row = i+1, column = 3)
        label5 = Label(tableFrame, text = data[4], borderwidth = 1, relief = "solid", height = 2, width = 20, padx = 5).grid(row = i+1, column = 4)
        i += 1

# Confirmation dialog of delete all data.
def clearAll():
    # Create top level window and its label.
    top = Toplevel()
    lbl = Label(top, text = "Yakin mau hapus semua data?")
    lbl.pack(padx = 20, pady = 20)

    # Create button frame.
    btnframe = LabelFrame(top, borderwidth = 0)
    btnframe.pack(padx = 20, pady = 20)
    
    # Accept button.
    btn_yes = Button(btnframe, text = "Gass", bg = "green", fg = "white", command = lambda:[top.destroy(), delAll()])
    btn_yes.grid(row = 0, column = 0, padx = 10)
    
    # Decline button.
    btn_no = Button(btnframe, text = "Tapi boong", bg = "red", fg = "white", command = top.destroy)
    btn_no.grid(row = 0, column = 1, padx = 10)

def viewFacility():
    # I don't know where I should put these functions, but I think it'll be
    # cleaner if I put it inside its parent function.
    
    # Go to previous "slide" of image.
    def prev_img(label):
        global img_index
        
        img_index -= 1
        if(img_index < 0):
            img_index = 4
        
        label = Label(frame, image = img_view).grid(row = 0, column = 1)

    # Go to next "slide" of image.
    def next_img(label):
        global img_index
        
        img_index += 1
        if(img_index > 4):
            img_index = 0
        
        label = Label(frame, image = img_view[img_index]).grid(row = 0, column = 1)

    # Hide root window.
    global root
    root.withdraw()

    # Create top-level window and its frame.
    top = Toplevel()
    top.title("Fasilitas Kampus")
    frame = LabelFrame(top, borderwidth = 0)
    frame.pack()

    # Initialize label.
    global img_index, img_name, img_view
    label = Label(frame, image = img_view[img_index]).grid(row = 0, column = 1)

    # Previous button.
    btn_prev = Button(frame, text = "<", anchor = "w", command = lambda:[prev_img(label)])
    btn_prev.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")

    # Next button.
    btn_prev = Button(frame, text = ">", anchor = "w", command = lambda:[next_img(label)])
    btn_prev.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = "w")

    # Cancel button.
    btn_cancel = Button(frame, text = "Kembali", anchor = "w", command = lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = "w")

# Confirmation dialog of exit program.
def exitDialog():
    # Hide root window.
    global root
    root.withdraw()

    # Create top level window and its label.
    top = Toplevel()
    lbl = Label(top, text = "Yakin mau keluar?")
    lbl.pack(padx = 20, pady = 20)

    # Create button frame.
    btnframe = LabelFrame(top, borderwidth = 0)
    btnframe.pack(padx = 20, pady = 20)
    
    # Accept button.
    btn_yes = Button(btnframe, text = "Gass", bg = "green", fg = "white", command = lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row = 0, column = 0, padx = 10)
    
    # Decline button.
    btn_no = Button(btnframe, text = "Tapi boong", bg = "red", fg = "white", command = lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row = 0, column = 1, padx = 10)

# Create title frame.
frame = LabelFrame(root, text = "Praktikum DPBO", padx = 10, pady = 10)
frame.pack(padx = 10, pady = 10)

# Create button group frame.
buttonGroup = LabelFrame(root, padx = 10, pady = 10)
buttonGroup.pack(padx = 10, pady = 10)

# Title.
label1 = Label(frame, text = "Data Mahasiswa", font = (30))
label1.pack()

# Description.
label2 = Label(frame, text = "Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input button.
b_add = Button(buttonGroup, text = "Input Data Mahasiswa", command = inputs, width = 30)
b_add.grid(row = 0, column = 0, pady = 5)

# Show all data button.
b_add = Button(buttonGroup, text = "Semua Data Mahasiswa", command = viewAll, width = 30)
b_add.grid(row = 1, column = 0, pady = 5)

# Clear all data button.
b_clear = Button(buttonGroup, text = "Hapus Semua Data Mahasiswa", command = clearAll, width = 30)
b_clear.grid(row = 2, column = 0, pady = 5)

# Show facility button.
b_facility = Button(buttonGroup, text = "Semua Fasilitas Kampus", command = viewFacility, width = 30)
b_facility.grid(row = 3, column = 0, pady = 5)

# Exit button.
b_exit = Button(buttonGroup, text = "Exit", command = exitDialog, width = 30)
b_exit.grid(row = 4, column = 0, pady = 5)

# Mainloop.
root.mainloop()