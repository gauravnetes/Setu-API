<script lang="ts">
	// This is where your JavaScript/TypeScript code goes.
	// We'll use this later to handle the search.
	let searchTerm = '';
</script>

<main class="relative flex min-h-screen flex-col items-center justify-center bg-zinc-900 p-4">
	<div
		class="py-30 rounded-4xl relative w-full max-w-4xl bg-zinc-800/10 px-36 text-center shadow-2xl"
	>
	
		<h1 id="logo" class="glow mb-5 text-5xl font-bold text-cyan-300">🐍 SETU API</h1>
		<p id="description" class="mb-5 mt-5 text-lg text-orange-300">
			Bridge India's Traditional Medicine to Global Standards
		</p>

		<div class="flex gap-2">
			<input
				id="search-input"
				type="text"
				bind:value={searchTerm}
				placeholder="Search for an Ayush term (e.g., Amlapitta)..."
				class="rounded-4xl focus:ring-3 flex-grow border-none bg-zinc-800 px-5 py-3 text-sm shadow-lg transition-all duration-300 focus:text-white focus:outline-none focus:ring-amber-600"
			/>
			<button
				id="search-button"
				class="rounded-4xl bg-orange-500 px-6 py-3 font-bold text-gray-100 shadow-lg transition-all duration-300 hover:bg-orange-600"
			>
				SEARCH
			</button>
		</div>
	</div>
</main>

<style>
	#logo,
	#search-button {
		font-family: 'Unbounded', sans-serif;
		font-optical-sizing: auto;
		font-weight: 500;
	}
	#description,
	#search-input {
		font-family: 'Space Mono', monospace;
	}

	.glow {
		text-shadow:
			0 0 5px currentColor,
			0 0 0px currentColor;
	}

</style>
