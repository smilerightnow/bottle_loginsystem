% rebase('base.tpl', title='Login')

<form action="/login" method="post">
	<input type="hidden" name="csrfmiddlewaretoken" value="{{csrf}}" />
    Email: <input name="email" type="text" />
    Password: <input name="password" type="password" />
    <input value="Login" type="submit" />
</form>
