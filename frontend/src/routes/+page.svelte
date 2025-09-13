<script lang="ts">
	let searchTerm = '';
	let isSearching = false;

	function handleSearch() {
		if (searchTerm.trim()) {
			isSearching = true;
			setTimeout(() => {
				isSearching = false;
			}, 1000);
		}
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleSearch();
		}
	}
</script>

<main class="relative flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white p-6">
	
	<!-- Header -->
	<div class="mb-8 text-center">
		<div class="flex items-center justify-center gap-3 mb-4">
			
			<h1 id="logo" class="text-5xl font-extrabold text-sky-500 tracking-tight glow">
				⚕️ SETU API
			</h1>
		</div>
		<p id="description" class="text-lg text-gray-600 mb-4">
			Bridge India's Traditional Medicine to Global Standards
		</p>
		<div class="text-sm text-gray-500 flex items-center justify-center gap-4">
			<span class="bg-blue-100 px-3 py-1 rounded-full">Ministry of AYUSH</span>
		</div>
	</div>

	<!-- Main Search Card -->
	<div class="w-full max-w-4xl bg-white rounded-3xl shadow-xl border-none p-8 mb-8">
		
		<!-- Search Bar -->
		<div class="flex gap-3 mb-6">
			<div class="relative flex-grow">
				<input
					id="search-input"
					type="text"
					bind:value={searchTerm}
					on:keypress={handleKeyPress}
					placeholder="🔍 Search for an AYUSH term (e.g., Amlapitta, Tridosha, Pranayama)..."
					class="w-full rounded-4xl border-none bg-blue-50 px-5 py-4 text-base shadow-sm transition-all duration-300 focus:border-sky-400 focus:ring-2 focus:ring-sky-300 focus:outline-none"
				/>
				{#if isSearching}
					<div class="absolute right-4 top-1/2 transform -translate-y-1/2">
						<div class="animate-spin w-5 h-5 border-2 border-sky-400 border-t-transparent rounded-full"></div>
					</div>
				{/if}
			</div>
			<button
				id="search-button"
				on:click={handleSearch}
				disabled={isSearching}
				class="rounded-4xl bg-sky-500 px-8 py-4 font-semibold text-white shadow-md transition-all duration-300 hover:bg-sky-600 hover:shadow-lg disabled:opacity-50"
			>
				{isSearching ? 'SEARCHING...' : 'SEARCH'}
			</button>
		</div>

		<!-- Quick Suggestions -->
		<div class="mb-8">
			<p class="text-sm text-gray-500 mb-3">Quick search:</p>
			<div class="flex flex-wrap gap-2">
				{#each ['Panchakosha', 'Tridosha', 'Marma', 'Rasayana', 'Pranayama', 'Chakra'] as suggestion}
					<button 
						class="px-4 py-2 bg-blue-100 text-sky-700 rounded-full text-sm hover:bg-blue-200 transition-colors border border-blue-200"
						on:click={() => searchTerm = suggestion}
					>
						{suggestion}
					</button>
				{/each}
			</div>
		</div>

		<!-- Feature Cards -->
		<div class="grid md:grid-cols-3 gap-6">
			<div class="text-center p-6 bg-blue-50 rounded-4xl border border-blue-100">
				<div class="w-12 h-12 bg-sky-500 rounded-full flex items-center justify-center text-white text-xl mx-auto mb-3">
					📚
				</div>
				<h3 class="font-semibold text-gray-800 mb-2">Traditional Terms</h3>
				<p class="text-sm text-gray-600">Comprehensive AYUSH terminology database</p>
			</div>
			
			<div class="text-center p-6 bg-blue-50 rounded-4xl border border-blue-100">
				<div class="w-12 h-12 bg-sky-500 rounded-full flex items-center justify-center text-white text-xl mx-auto mb-3">
					🌐
				</div>
				<h3 class="font-semibold text-gray-800 mb-2">Global Standards</h3>
				<p class="text-sm text-gray-600">Mapped to international classifications</p>
			</div>
			
			<div class="text-center p-6 bg-blue-50 rounded-4xl border border-blue-100">
				<div class="w-12 h-12 bg-sky-500 rounded-full flex items-center justify-center text-white text-xl mx-auto mb-3">
					🔗
				</div>
				<h3 class="font-semibold text-gray-800 mb-2">Easy Integration</h3>
				<p class="text-sm text-gray-600">Simple API for healthcare systems</p>
			</div>
		</div>
	</div>


	<!-- Footer -->
	<div class="text-center text-gray-500">
		<p class="text-sm">Empowering Traditional Medicine Through Technology</p>
	</div>
</main>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

	#logo,
	#search-button {
		font-family: 'Unbounded', sans-serif;
		font-optical-sizing: auto;
	}
	
	#description,
	#search-input {
		font-family: 'Space Mono', monospace;
	}

	.glow {
		text-shadow: 0 0 8px rgba(56, 189, 248, 0.3);
	}
</style>