$(document).ready(() => {

  let citySearchInput = $('.js-city-autocomplete-input')
  let hiddenCityInput = $('.js-city-autocomplete-hidden')

  let loading = $('.js-city-autocomplete-loading')
  let noLoading = $('.js-city-autocomplete-no-loading')

  citySearchInput
    // https://api.jqueryui.com/autocomplete/
    .autocomplete({
      delay: 300,
      minLength: 1,
      source: citySearchInput.data('autocomplete-source-url'),
      autoFocus: true,
      // Make a selection on focus.
      focus: (event, ui) => {
        hiddenCityInput.val(ui.item.slug)  // Store city slug.
        hiddenCityInput.data('title', ui.item.value)  // Store city name.
      },
      // When the menu is hidden (usually when the form is submitted)
      // populate citySearchInput with the city name so that it is part
      // of the querystring.
      close: (event, ui) => {
        let value = hiddenCityInput.data('title')
        if (value) {
          citySearchInput.val(value)
        }
      },
      // Allow to submit the parent form when the enter key is pressed.
      select: (event, ui) => {
        if (event.keyCode === 13) {
          let value = hiddenCityInput.data('title')
          citySearchInput.val(value)
          citySearchInput.parents('form:first').submit()
        }
      },
      search: (event, ui) => {
          loading.addClass('d-block')
          noLoading.addClass('d-none')
      },
      response: (event, ui) => {
          loading.removeClass('d-block')
          noLoading.removeClass('d-none')
      },
    })
    .keypress(e => {
      if (e.keyCode === 27) {
        citySearchInput.val('')
      }
    })
    .focus(() => {
      citySearchInput.val('')
      hiddenCityInput.val('')
    })

})
