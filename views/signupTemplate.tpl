% rebase('base.tpl', title='Signup')

<form action="/signup" method="post">
	<input type="hidden" name="csrfmiddlewaretoken" value="{{csrf}}" />
    Email: <input name="email" type="text" />
    Username: <input name="username" type="text" />
    Password: <input name="password" type="password" />
    <input value="Signup" type="submit" />
</form>
