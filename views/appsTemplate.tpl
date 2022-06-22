% rebase('base.tpl', title='Apps', user=user)
<h1>Hello {{user["username"]}} at Apps list!</h1>

% for app in appsList:
	<p>{{app.title}}</p>
% end
