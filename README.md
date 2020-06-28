
## CROWDSOURCING
Crowdsourcing adalah sebuah istilah yang sering digunakan untuk menggambarkan suatu proses dalam mendapatkan pekerjaan atau pendanaan dari sekelompok orang dalam jumlah banyak melalui fasilitas online. Konsep yang digunakan untuk menjalankan teknik ini adalah dengan tersedianya orang-orang dalam kelompok besar untuk menghasilkan konten atau pendanaan
Ruang lingkup dari project ini yaitu untuk membuat aplikasi sosial media crowdsourcing berbasis website dengan bahasa pemrograman Python, menggunakan database SQL Lite, dan framework Django

## About Django
With Django, you can take Web applications from concept to launch in a matter of hours. Django takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.
Django takes the pain out of development by easing common tasks used in many web projects, such as:
- https://docs.djangoproject.com/en/3.0/

## Consist of 2 Actors
-Pengunjung yang masuk ke web ini dapat melakukan register, login, melihat postingan dan detailnya, serta memfilter postingan berdasarkan kategori dan kata pencarian
-Pengguna dari website ini dapat melakukan semua yang dilakukan oleh pengunjung, dan terdapat tambahan seperti edit profil, ubah password akun, create project, edit project, delete project, melihat post yang di-like, mengomentari project, memberikan like dan dislike pada komentar maupun pada postingan project, dan logout.

## Installation
1.	Install Python 3.7.3 (pastikan untuk mencentang add to PATH)
2.	Pada command prompt ketikan perintah berikut:
```
- mkdir AgileRE (untuk membuat direktori baru [tidak harus pada disk C:])
- cd AgileRE
- python -m venv env
- git clone https://github.com/AgileRE/Crowd2020.git
- env\scripts\activate.bat
- cd Crowd2020
- pip install -r req.txt
- Tunggu beberapa saat sampai instalasi semua dependensi berhasil

```
3. Buka file explorer
4. Menuju alamat:
- [alamat lokal (No.2a)]\ env\Lib\site-packages\qurl_templatetag\qurl.py
(hal ini dilakukan karena perbedaan python version yang digunakan antara program dengan library yang digunakan -Januari 2020)
5. Ubah line ke-2 baris koding menjadi import six
6. Pada command prompt ketikan perintah berikut:
```
- python manage.py migrate
- python manage.py runserver
- Menuju browser dengan alamat http://127.0.0.1:8000/
```
Program dapat berjalan dengan tampilan awal sebagai berikut:

## How It Works
```
Login dan Register
- Masuk halaman login atau register akun.
- Lakukan login untuk masuk kedalam Dashboard.
- Apabila pengguna lupa password maka klik Forget password dan akan dikirim melalui email pengguna.
- Halaman dashboard timeline yang memungkinkan pengunjung untuk melihat postingan project .Halaman dashboard dapat diakses dengan atau tanpa melakukan login.
- Pengunjung yang melakukan login (Pengguna) memungkinkan untuk melihat postingan project orang lain dan memberikan kontribusi dengan melihat detail project.
- Halaman detail postingan project. Pengguna dapat melihat detail postingan project, memfilter postingan berdasarkan kategori, dan memfilter postingan berdasarkan kata pencarian. Pengguna dapat melihat detail postingan project, memberikan like dan dislike pada project, menonaktifkan project miliknya, memfilter postingan berdasarkan kategori, dan memfilter postingan berdasarkan kata pencarian. 
- Pengguna dapat memberikan komentar user requirement dengan memilih kategori fungsional dan non fungsional .Setiap pengguna dapat memberikan like atau dislike pada komentar. Serta dapat menambahkan komentar pada diskusi requirement.

Profile
- Pada menu pengguna terdapat pilihan Profile, My Project, Like Contributions.
- Pada halaman Profile , pengguna dapat mengubah informasi profile.
- Pada halaman My Project , pengguna dapat melihat project-projectnya.
- Pada halaman Like , pengguna dapat melihat project-project yang disukai.
- Pada halaman Contribution, pengguna dapat melihat kontribusi user requirement pada project-project lain.

Posting
- Pada halaman Posting, pengguna dapat menuliskan atau mengunggah ide project dengan mengubah status project, mengisi judul, ringkasan project, detail project , menambahkan gambar serta memilih kategori.
- Pengguna juga dapat mengedit project dengan masuk ke halaman edit project dengan mengubah status menjadi close atau lainnya.
- Kemudian setelah mendapatkan banyak masukan atau tanggapan user requirement dari pengguna lain , maka setelah dirasa cukup dapat menutup project dengan mengubah status project dan melakukan approve/decline tanggapan user requirement pada projectnya.
- Lalu untuk mendapatkan laporan dari user requirement dapat menekan report pada project dan mendapatkan file dalam bentuk pdf untuk disimpan

```
## Contributors
- Qurrota 'Ayun Saskhiyah 081611633002
- Muhammad Luthfan O.S. 081711633002
- Annisa Anjani 081711633004
- Karunia Amalia Tirta 081711633008
- Manis Hanggraeni 081711633012
- Fahima Lailul Ula 081711633017
- Dyah Ayu Permatasari 081711633024
- Robby Dwi Angga P. 081711633028
- Araeyya yenofa putri 081711633031
- Prastowo Budiartha 081711633033
- Fachrizal Fikri 081711633042
- Aprilia Putri Ariesta 081711633049
- I Nyoman Dedi F.A. 081711633053
