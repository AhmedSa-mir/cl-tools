<script>
	//import { onMount } from 'svelte';
	import Nav from './components/Nav.svelte';
	import Homepage from './components/Home.svelte';
	import Proclistpage from './components/ProcList.svelte';   
	import Todopage from './components/Todo.svelte';
 
	export let appName;
	export let selectedTab = 'home';

	// onMount(async () => {
		
	// });


	function switchTab(event) {
		selectedTab = event.detail.text;
	}

</script>

<div id="page">
	<Nav on:tabpress={switchTab}/>
	<main id="pagecontent">
		{#if selectedTab === 'proc'}
			<Proclistpage/>
		{:else if selectedTab === 'todo'}
			<Todopage/>
		{:else}
			<Homepage {appName}/>
		{/if}
	</main>
</div>


<style>
	#page{
		height: 100%;
	}
	#pagecontent {
		height: 90%;
		display: flex;
	}
</style>