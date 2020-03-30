<script>
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';

  export let appName;
  let visible = true;
  let interval;

  onMount(() => {
		interval = setInterval(function(){ visible=!visible }, 800);
  });
  
  onDestroy(() => clearInterval(interval));
  
</script>

<div class='homepage container'>
  <div class="row">
    <h1 >Welcome to {appName}</h1>
  </div>
  <div class="row">
    {#if visible}  
      <p transition:fade="{{duration: 500}}">
      <i transition:fade="{{duration: 500}}" class="fa fa-terminal align-middle" style="font-size:48px;"></i>
      where you can execute commands</p>
    {:else}
      <p></p>
    {/if}
  </div>
</div>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.row {
  height: 120px;
}

h1 {
  font-size: 5em;
  font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  font-weight:bold;
}

p {
  font-size: 200%;
  font-family:monospace;
}
</style>