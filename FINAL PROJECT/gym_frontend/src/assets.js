// Free-to-use photos from Wikimedia Commons (Special:FilePath gives a stable
// direct link to the current version of a file, which is why we use it here
// instead of a raw upload.wikimedia.org URL).
const commons = (file) => `https://commons.wikimedia.org/wiki/Special:FilePath/${file}`

export const HERO_IMAGE = commons('Gym_wiki.jpg')

export const EQUIPMENT_HERO = commons('Free_weight.jpg')
export const SUPPLEMENT_HERO = commons('Bodybuilding_supplement_high_protein_drink_mix_700g.jpg')

// Individual product photos aren't stored by the backend, so we show a
// photo based on the item's category instead of a per-product image.
const EQUIPMENT_CATEGORY_PHOTOS = [
  { match: /cardio|tread|run|bike|cycle|row/i, photo: commons('Sandown_outdoor_gym_treadmill.JPG') },
  { match: /dumbbell|weight|strength|plate/i, photo: commons('Dumbbell.JPG') },
  { match: /bench|rack|machine/i, photo: commons('Free_weight.jpg') },
]
export const EQUIPMENT_DEFAULT_PHOTO = commons('Dumbbells_in_a_local_Gym.jpg')

const SUPPLEMENT_CATEGORY_PHOTOS = [
  { match: /whey|protein/i, photo: commons('Protein_shake.jpg') },
  { match: /gainer|mass|carb/i, photo: commons('Bodybuilding_supplement_high_protein_drink_mix_700g.jpg') },
]
export const SUPPLEMENT_DEFAULT_PHOTO = commons('Whey_powder.jpg')

export function equipmentPhoto(category = '') {
  const found = EQUIPMENT_CATEGORY_PHOTOS.find((c) => c.match.test(category))
  return found ? found.photo : EQUIPMENT_DEFAULT_PHOTO
}

export function supplementPhoto(category = '') {
  const found = SUPPLEMENT_CATEGORY_PHOTOS.find((c) => c.match.test(category))
  return found ? found.photo : SUPPLEMENT_DEFAULT_PHOTO
}
