let provider_butts = document.querySelectorAll(".provider_menu_butt")
let provider_tabs = document.querySelectorAll(".provider_tab")

provider_butts.forEach(provider_butt => {
    provider_butt.addEventListener('click', () => {
        provider_butts.forEach(butt => {
            butt.classList.remove("provider_menu_butt_active");
        });

        provider_tabs.forEach(tab => {
            tab.classList.remove("provider_tab_active");
        });


        provider_butt.classList.add("provider_menu_butt_active");
        provider_tabs[provider_butt.dataset.tab].classList.add("provider_tab_active");
    });
});
