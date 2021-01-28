# from flask import Blueprint,render_template,request,session,redirect,url_for

# admin = Blueprint('admin',__name__,template_folder='templates')


# @admin.route('/')
# def index():
# 	if not islogget():
# 		redirect(url_for('.login'))
# 	return render_template('admin/admin_index.html')

# # функция авторизации админа используется в обработчике авторизации	
# def login_admin():
# 	session['admin_logged'] = 1

# #функция проверки авторизации админа , используется в обработчике logout
# def islogget():
# 	return True if session.get('admin_logged') else False


# #функция выходи из админки используется в обработчике logout
# def logout_admin():
# 	session.pop('admin_logged',None)


# #Обработчик авторизации админа
# @admin.route('/login', methods=['POST','GET'])
# def login():
# 	#Проверка не авторизирован ли уже пользователь
# 	if islogget():
# 		return redirect(url_for('.index'))

# 	if request.method == 'POST':
# 		if request.form['user'] == 'admin' and request.form['pws'] == 'qwerty':
# 			login_admin()
# 			return redirect(url_for('.index'))
# 		else:
# 			flash('Неверная пара логин и пароль','error')
# 	return render_template('admin/login.html',title='Админ-панель')
# #Обработчик выхода из админки 
# @admin.route('/logout')
# def logout():
# 	if not islogget():
# 		return redirect(url_for('.login'))
# 	logout_admin()
# 	return redirect(url_for('.login'))