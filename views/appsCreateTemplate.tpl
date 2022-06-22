% rebase('base.tpl', title='Create an app', user=user)
<h1>Create an App!</h1>

<form action="/apps/create" method="post">
	<input type="hidden" name="csrfmiddlewaretoken" value="{{csrf}}" />
	<label for="title">Title:</label>
    <input id="title" name="title" type="text" />
    <label for="type">Type:</label>
	<input id="type" name="type" type="text" />
	<label for="data">Data:</label>
	<input id="data" name="data" type="text" />
    <input value="Done" type="submit" />
</form>

