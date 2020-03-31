<script>
	import { selectedTab } from '../components/stores.js';
	import HomePage from './Home.svelte';
	import ProcListPage from './ProcList.svelte';   
	import TodoPage from './Todo.svelte';
 
	let appName = '3Bot CLI';
</script>


{#if $selectedTab === 'proc'}
	<ProcListPage/>
{:else if $selectedTab === 'todo'}
	<TodoPage/>
{:else}
	<HomePage {appName}/>
{/if}


<style>
</style>