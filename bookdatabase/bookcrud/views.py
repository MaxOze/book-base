from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def start(request):                 # Нужно чтобы просто отправляло на страницу авторизации при пустой ссылке
    return HttpResponseRedirect('/signin')

# Render
def index(request):
    books = BooksappBook.objects.all()

    paginator = Paginator(books, 3)
    page = request.GET.get("page")

    try:
        page_books = paginator.get_page(page)
    except PageNotAnInteger:
        page_books = paginator.get_page(1)
    except EmptyPage:
        page_books = paginator.get_page(paginator.num_pages)

    for book in page_books:
        print(book.book_name)

    data = {"page": page, "page_books": page_books, 'role': request.session.get('role', 'none'), 'name': request.session.get('name', '')}

    return render(request, "index.html", context=data)

# Create
def create(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return HttpResponseRedirect('/signin')          # Если не зареган то отправляет авторизовываться

    if request.method == "GET":
        form = BookForm()
        data = {"form": form}

        return render(request, "create.html", context=data)

    form = BookForm(request.POST)
    if form.is_valid():
        form.save()

    return HttpResponseRedirect("/")

# Edit
def edit(request, id):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'admin':
        return HttpResponseRedirect('/shop?page=1')         # Если не админ то не может менять книги

    try:
        book = BooksappBook.objects.get(id=id)

        if request.method == "POST":
            form = BookForm(request.POST)    # Достает из формы данные
            if form.is_valid():                             # Проверяет валидность данных
                form.save() 

            return HttpResponseRedirect("/")
        else:
            form = BookForm(instance=book)
            data = {"form": form}

            return render(request, "edit.html", context=data)
    except BooksappBook.DoesNotExist:
        return HttpResponseNotFound("<h2>Book doesnt exist</h2>")

# Delete
def delete(request, id):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'admin':
        return HttpResponseRedirect('/shop?page=1')         # Если не админ то не может удалять книги

    try:
        book = BooksappBook.objects.get(id=id)
        book.delete()

        return HttpResponseRedirect("/")
    except BooksappBook.DoesNotExist:
        return HttpResponseNotFound("<h2>Book doesnt exist</h2>")


# Registration
def signUp(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'none':
        return HttpResponseRedirect('/shop?page=1')         # Если уже авторизован то отправляет на главную страницу

    if request.method == 'POST':                            # Если форма заполнена
        form = UserSignUpForm(request.POST)                 # Берет данны из формы
        if form.is_valid():
            user = BooksappUser()
            user.name = form.cleaned_data['name']           # Достает данные из формы
            user.email = form.cleaned_data['email']         # Достает данные из формы
            user.login = form.cleaned_data['login']         # Достает данные из формы
            user.password = form.cleaned_data['password']   # Достает данные из формы
            user.role = BooksappRole.objects.get(id=1)              # Дает ему роль обычного юзера (админ только один с логином и паролем admin)
            user = user.save()                              # Сохраняет нового юзера в базу

            return HttpResponseRedirect('/signin')
    else:
        form = UserSignUpForm()                             # Если первый раз страниц открыта то выводит пустую форму

    return render(request, 'sign_up.html', {'form': form})


# Authorization
def signIn(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'none':
        return HttpResponseRedirect('/shop?page=1')         # Если уже авторизован то отправляет на главную страницу

    if request.method == 'POST':                        # Если форма заполнена
        form = UserSignInForm(request.POST)             # Достает данные из формы
        if form.is_valid():                             # Если форма норм заполнена
            if BooksappUser.objects.filter(login=form.cleaned_data['login']).exists():      # Проверяет есть ли чел с таким логином
                user = BooksappUser.objects.get(login=form.cleaned_data['login'])           # Если есть то достает его из базы данных
                if (user.password == form.cleaned_data['password']):                # Сверяет его пароль с введеным паролем
                    request.session['name'] = user.name                 # Создает в сессии имя пользователя
                    request.session['role'] = user.role.role_name            # Создает в сессии роль пользователя
                    request.session['cart'] = list()                    # Создает в сессии корзину
                    return HttpResponseRedirect('/')                                # Отправляет на главную страницу
                else:
                    result = 'Неправильный пароль'          # Если пароль неправильный
            else:
                result = 'Несуществующий логин'             # Если такого логина нет
            form = UserSignInForm()                         # Если что то не так то просто выводит пустую форму

            return render(request, 'sign_in.html', {'form': form, 'result': result})    # Передает форму и сообщение если что то не так
    else:
        result = ' '
        form = UserSignInForm()         # Выводит пустую форму если зашли на страницу в первый раз

        return render(request, 'sign_in.html', {'form': form, 'result': result})    # result - это строчка которая пустая если все норм или пишет в чем ошибся пользователь


# Unautharization
def logout(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'none':
        del request.session['role']         # Если был авторизован то удаляет все данные из сессии и отправляет на авторизацию
        del request.session['name']
        del request.session['cart']
    return HttpResponseRedirect('/signin')
    

# Profile
def profile(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return HttpResponseRedirect('/signin')      # Если не зареган то отправляет авторизовываться

    user = BooksappUser.objects.get(name=request.session['name'])           # Достает из сессии имя пользователя
    if request.method == 'POST':                                    # Если нажали изменить данные
        form = UserEditForm(request.POST, instance=user)            # Достает из формы данные
        if form.is_valid():                                         # Если данные валидны
            user.name = form.cleaned_data['name']                   # Достает из формы данные
            user.email = form.cleaned_data['email']                 # Достает из формы данные
            user = user.save()                                      # Сохраняет данные о пользователе в базу
            request.session['name'] = form.cleaned_data['name']     # Меняет имя пользователя в сессии

            return HttpResponseRedirect('/profile')                             # Снова открывает эту страницу с обновленными данными
    else:
        form = UserEditForm(instance=user)          # Если открыли только открыли то показывает форму с теми данными которые есть
    
    return render(request, "profile.html", {'form': form})


# Adding to cart
def toCart(request, id):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return HttpResponseRedirect('/signin')      # Если не зареган то отправляет авторизовываться

    if BooksappBook.objects.filter(id=id).exists():         # Проверяет есть ли такая книга
        cart = request.session['cart']              # Берет корзину из сессии
        cart.append(id)                             # Добавляет в корзину id книги
        request.session['cart'] = cart              # Засовывает корзину обратно в сессию
        page_number = request.GET.get('page')       # Смотрит с какой страницы был сделан запрос на эту книгу чтобы потом вернуть на нее обратно

    return HttpResponseRedirect("/shop?page="+page_number)      # Возвращает на нужную страницу


# Cart
def cart(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return HttpResponseRedirect('/signin')              # Если не зареган то отправляет авторизовываться

    cart = request.session['cart']              # Достает из сессии корзину
    books = list()                              # Список для книг
    fullprice = 0                               # Переменная для подсчета полной цены корзины
    for id in cart:                             # Для каждого id книги из корзины:
        book = BooksappBook.objects.get(id=id)              # Берет из базы книгу по id
        books.append(book)                          # Добавляет ее в список
        fullprice = fullprice + book.price          # Добавляет ее цену

    if request.method == 'POST':                                        # Если нажали "сделать заказ"
        order = BooksappOrder()                                                 # Создает заказ
        order.order_user = BooksappUser.objects.get(name=request.session['name'])     # Ищет юзера который этот заказ сделал по имени из сессии
        order.order_price = fullprice                                         # Добавляет полную цену заказа
        order.save()                                                    # Сохраняет заказ в таблицу orders

        for id in cart:                                     # Для каждого id книги из корзины:
            orderBook = BooksappOrderBook()                         # Создает отношение заказ-книга (для таблицы которая связывает заказ и книги)
            orderBook.order = BooksappOrder.objects.last()          # Берет id заказа который мы последним (только что)
            orderBook.book = BooksappBook.objects.get(id=id)        # Связывает его с id книги
            orderBook.save()                                # Сохраняет в таблицу orders_books

        request.session['cart'] = list()                # Очищает корзину

        return render(request, 'success.html')          # Перенаправляет на страницу с сообщение об успешном заказе

    context = {
        'books': books,                         # Достает из куки корзину пользователя
        'name': request.session['name'],        # Достает из куки сессии имя
        'fullprice': fullprice,
    }

    return render(request, 'cart.html', context)


# Orders
def orders(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return HttpResponseRedirect('/signin')              # Если не зареган то отправляет авторизовываться

    user = BooksappUser.objects.get(name=request.session['name'])   # Достает из сессии юзера который делает заказ
    userOrders = BooksappOrder.objects.filter(order_user=user)            # Достает заказы этого юзера
    orders = dict()                                         # Словарь который потом пойдет в html
    i = 1                    # Переменная для номера заказа                            
    for item in userOrders:                                 # Для каждого заказа:
        order = BooksappOrderBook.objects.filter(order=item)            # Достает все соотношения заказ-книга
        books = list()                                          # Список книг для каждого заказа
        for book in order:                                      # Для каждого этого отношения:
            books.append(book.book)                                 # Добавляет книги из заказа

        orders['# ' + str(i) + ' ' + str(item.order_date)[:19] + ' | ' + str(item.order_price)] = books     # Добавляет словарь книг к заказу в список заказов
        i = i + 1                                                                                # Где ключ будет в заголовке с датой и ценой заказа
                                                                                                 # А значение это книги которые в заказе
    return render (request, 'orders.html', {'orders': orders})
