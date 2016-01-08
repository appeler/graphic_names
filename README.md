## Clarifai the Gender of a Name

Are men covered more often in business news than women? To answer the question and questions like these using text corpora, we need a way to infer gender based on the (first) name. In the US, one can easily infer the gender based on the first name using the data made available by the SSA and the Census. No such comparable data, however, exists for many other countries (and languages). 

Here we investigate a way of getting such data for 'Indian' names. We pair Google image search (via Google custom search API) with [clarifai.com](http://clarifai.com). In particular, we search for images using first names, and then get tags of those images via [clarifai](http://clarifai.com). We next count tags carrying information about gender--- man, men, boy, woman, women, girl. And classify based on whether 'male' tags are more common (probable) than 'female'. We validate the method using a dataset of names for which the gender is known. 

A few caveats and notes:   
1. Images that we find via Google image search are not constrained to a country (though this constraint can be added).   
2. Images returned by Google image search are sometimes close replicas, if not duplicates, of each others. This should not matter, but it is something to be aware of.   
3. Even if we were to get images hosted on websites located in a country (or some version of this), they would still not a representative set of people (in a country, in that language) with that name.   
4. Most names are not given uniquely to males or females. Instead, there is a distribution. For instance, some people named Jesse are men, others women. We elide over this point in the validation exercise. If we had good data on gender of first names, we wouldn't be doing all this to begin with.   
5. The gender distribution of a name changes over time, and by country.   
6. Some information about the gender associated with a name in countries (languages) where we don't have data may be recovered from SSA and Census data in US, and similar such data from other countries by exploiting the fact that these countries attract immigrants from various countries. For instance, one can infer gender of the name 'Gaurav' via [https://api.genderize.io/?name=gaurav](https://api.genderize.io/?name=gaurav).   
7. Inferring gender based on a limited set of tags returned by clarifai is still a clunky way of getting data about gender from images. Read more [here](http://gbytes.gsood.com/2015/12/31/clarifaing-the-future-of-clarifai-some-thoughts/) on that.   
8. Rather than use clarifai alone, it may be a better idea to use it as one of the signals for a more general classifier. For instance, building a general inferential engine that uses clarifai, but also these available data from other countries and whether male/female pronouns are more common in sentences using that name.      

----

Begin by installing the requirements:

```
pip install -r requirements.txt
```

PhantomJS is required for [Google Image Search](google_image_search.py) script. If you don't have it installed, type in:

```
apt-get install phantomjs
```

Next, use [Google Image Search](scripts/google_image_search/) to find images associated with a name. To get tags for each of the images from clarifai, use [get clarifai tags](scripts/get_clarifai_tags/).  

### Validation

To assess the validity of the method, we use a dataset of people whose gender is known --- dataset on [Indian political candidates (myNeta)](https://github.com/soodoku/indian-politician-bios). We first took a [stratified random sample](scripts/utils/) of 1000 men and 1000 women. And then used [Google Image Search](scripts/google_image_search/) to search for first names, getting the URL of as many images as 100 images for each first name. ([Output file (bz2 format)](validate/output-img-(1000%2B1000).csv.bz2)). In total, we get 1956 names which have 100 or more images. Of the 44 remaining, there are 5 names for which we find no images (AWALASAKAR, MULAISWORI, RUKHIYABANO, VANLALHMINGCHHUANGI, SOMLANAIKA). Some of these problems are clearly due to badly formatted names. RUKHIYABANO for instance should read as Rukhiya Bano. Next, we signed up for a [clarifai API](http://clarifai.com) plan that allowed us to tag 100k images. We utilized our plan as follows: Of the 1956 rows, we further got a stratified sub-sample of 1500 names (750 M, 750 W). To max. out the 100k image quota, and to get some variation in number of images per name --- varying the number of images we tag per name allows us to test whether accuracy increases as we get tags for more images, we tried to tag the first 50 images each for 750 names, first 75 images each for 500 names, and first 100 images for 250 names. However, we didn't account for the fact that clarifai doesn't tag images that aren't jpeg or png and ended up with a small shortfall. In two cases for which we wanted to tag 75 images --- RAMFANGZAUVI and SANDHYATAI --- we only could tage 72 and 70 images respectively. The final output (bz2): [250 names X 100](validate/output-img-tag-250x100.csv.bz2), [500 names X 75](validate/output-img-tag-500x75.csv.bz2) and [750 names X 50](validate/output-img-tag-750x50.csv.bz2). Next, we classify the name as female if probability of 'female' tags (woman, women, female, girl) is greater than 'male' tags (man, men, male, boy). The classification success is about 77%. We also plot word clouds for men and women. (See [here](validate/valid.md).) As we note above, more information returned for each of the images can be used for classification. For instance, a classifier can be created that exploits other tags, such as jewellery etc. to infer the gender of people in the photos.  

### License
Released under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/).