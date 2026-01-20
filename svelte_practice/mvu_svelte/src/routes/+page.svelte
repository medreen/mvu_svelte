<script lang='ts'>
	import { goto } from '$app/navigation';
    let {data} = $props();
</script>

{#snippet button(text:string, onclick: any)}
        <button type="button" {onclick} class="h-9 px-2 rounded-md bg-amber-900 text-white font-bold hover:bg-amber-800">{text}</button>    
{/snippet}

<section>
    <h1 class="text-2xl text-amber-800 font-extrabold">Departments</h1>
    <div class="mb-4">
        <input type="text" placeholder="Search..." class="border border-amber-800 rounded-md h-9 p-2"/>
        {@render button('Search',()=>{})}
        {@render button('Edit',()=>{})}
    </div>

    {#each data.departments as department}
    <div class="flex odd:bg-amber-800 items-center gap-3.5 p-2">
        {@render button('Edit', ()=> {goto('department/'+department.department_id)})}
        {department.department_name}
    </div>        
    {/each}

    {#if data.departments.length === 0}
        <div class="p-4 bg-amber-800">No departments found, add one above</div>
    {/if}

</section>
