<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	function handleClick(tab) {
		dispatch('tabpress', {
			text: tab
		});
	}
</script>

<nav class="navbar navbar-fixed-left">
	<div class="container-fluid">
		<div class="navbar-header">
			<a type="button" class="navbar-brand"
				on:click={() => handleClick("home")}>3Bot CL</a>
		</div>
		<ul class="nav navbar-nav">
			<li class="active"><a type="button"
				on:click={() => handleClick("home")}>Home</a>
		</ul>
		<ul class="nav navbar-nav">
			<li><a type="button"
				on:click={() => handleClick("proc")}>List Processes</a></li>
		</ul>
		<ul class="nav navbar-nav">
			<li><a type="button"
				on:click={() => handleClick("todo")}>Todo</a></li>
		</ul>
	</div>
</nav>

<style>
</style>