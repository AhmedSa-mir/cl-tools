<script>
	import { selectedTab } from './stores.js';

	function switchTab(tab) {
		$selectedTab = tab;
	}
</script>

<nav class="navbar navbar-fixed-left">
	<div class="container-fluid">
		<div class="navbar-header">
			<a type="button" class="navbar-brand" href="."
				on:click={() => switchTab("home")}>3Bot CLI</a>	
		</div>
		<ul class="nav navbar-nav">
			<li class="active"><a type="button" href="."
				on:click={() => switchTab("home")}>Home</a>
		</ul>
		<ul class="nav navbar-nav">
			<li><a type="button" href="."
				on:click={() => switchTab("proc")}>List Processes</a></li>
		</ul>
		<ul class="nav navbar-nav">
			<li><a type="button" href="."
				on:click={() => switchTab("todo")}>Todo</a></li>
		</ul>
	</div>
</nav>

<style>
</style>