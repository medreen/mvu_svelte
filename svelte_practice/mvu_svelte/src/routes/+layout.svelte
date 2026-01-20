<script lang="ts">
	import '../app.css';
	import logo from '$lib/assets/logo.png';
	
	let { children } = $props();
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
	<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
</svelte:head>

<!-- Warm brown background -->
<div class="min-h-screen bg-amber-50" style="font-family: 'Poppins', sans-serif;">
	<!-- Centered main content with max width -->
	<div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
		<!-- Top nav bar - clean and minimal -->
		<nav class="py-6 flex items-center justify-between">
			<!-- Left Logo -->
			<div class="flex items-center gap-3">
				<img src={logo} alt="Logo" class="h-8 md:h-10 w-auto" />
				<span class="text-xl md:text-2xl font-semibold text-amber-900">
					Eclectic
				</span>
			</div>
			
			<!-- Right nav items (optional) -->
			<div class="flex items-center gap-4">
				<button class="px-4 py-2 text-sm font-medium text-amber-800 hover:text-amber-950 transition-colors">
					About
				</button>
				<button class="px-5 py-2 text-sm font-medium text-white bg-amber-700 hover:bg-amber-800 rounded-full hover:shadow-lg hover:scale-105 transition-all">
					Get Started
				</button>
			</div>
		</nav>

		<!-- Main content card -->
		<main class="pb-8">
			<div class="bg-white rounded-3xl shadow-xl shadow-amber-200/50 p-6 md:p-8 lg:p-10 min-h-[500px] border border-amber-100">
				{@render children()}
			</div>
		</main>

		<!-- Footer (optional) -->
		<footer class="py-6 text-center text-sm text-amber-800">
			<p>© 2026 Your Company. All rights reserved.</p>
		</footer>
	</div>
</div>