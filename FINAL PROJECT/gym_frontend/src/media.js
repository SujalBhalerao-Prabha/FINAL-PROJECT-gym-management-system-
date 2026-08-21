// Photos are served from Wikimedia Commons via Special:FilePath, which is a
// stable redirect straight to the current file — no API key needed, and it
// won't 404 the way a guessed stock-photo ID can. All of these are
// freely-licensed (CC / public domain) photos.
const commons = (file) =>
  `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(file)}`

export const heroImage = commons('Gym wiki.jpg')

export const equipmentImages = {
  'Gym Essentials': commons('Dumbbell.JPG'),
  'Workout Accessories': commons('Free weight.jpg'),
  'Personal Care': commons('Upright row with kettle bell.jpg'),
  'Useful Extras': commons('Sandown outdoor gym treadmill.JPG'),
  default: commons('Dumbbells in a local Gym.jpg')
}

export const getEquipmentImage = (category) =>
  equipmentImages[category] || equipmentImages.default

export const supplementImages = {
  Protein: commons('Protein shake.jpg'),
  Vitamins: commons('Whey powder.jpg'),
  'Weight Gain': commons('Bodybuilding supplement high protein drink mix 700g.jpg'),
  'Pre-Workout': commons('Whey powder.jpg'),
  Other: commons('Bodybuilding supplement high protein drink mix 700g.jpg'),
  default: commons('Protein shake.jpg')
}

export const getSupplementImage = (category) =>
  supplementImages[category] || supplementImages.default

// A couple of short, freely-licensed (CC0) demo clips just to show what
// "equipment videos" looks like in the UI — generic sample footage, not
// real product demos, since we don't have licensed footage of the actual
// gym equipment to embed.
export const equipmentVideos = [
  {
    title: 'Sample equipment video 1',
    src: 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4'
  },
  {
    title: 'Sample equipment video 2',
    src: 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/friday.mp4'
  }
]
