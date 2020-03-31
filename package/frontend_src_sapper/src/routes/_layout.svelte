<script>
	import Nav from '../components/Nav.svelte';
</script>

<style>
	#page{
		height: 100%;
	}
	main {
		height: 90%;
		display: flex;
		background-color: white;
		padding: 2em;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>

<Nav/>

<div id="page">
	<main id="pagecontent">
		<slot></slot>
	</main>
</div>