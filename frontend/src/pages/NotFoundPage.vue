<template>
  <div class="flex flex-col items-center justify-center md:gap-8 gap-6 md:py-24 py-12 max-w-225 w-full self-center grow basis-full container text-white text-center">
    <div class="flex flex-col gap-3 items-center">
      <h1 class="md:text-7xl text-[56px] font-medium leading-[100%]">404</h1>
      <h2 class="md:text-5xl text-[28px] font-medium leading-[120%]">
        Страница не найдена
      </h2>
      <p class="md:text-xl text-base font-light leading-[140%] text-text-secondary max-w-[640px]">
        Возможно, страница была перемещена, удалена или ссылка введена неверно.
      </p>
    </div>

    <RouterLink
      to="/"
      class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 outline-none bg-brand hover:bg-brand-hover text-text-primary md:p-6 p-4.5 max-md:rounded-[22px]"
    >
      <span class="md:text-xl text-base font-medium leading-[140%] px-1">
        На главную
      </span>
    </RouterLink>
  </div>
</template>