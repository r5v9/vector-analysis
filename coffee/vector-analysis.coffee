fs = require('fs')

sum = (list) ->
    if list.length == 0 then 0 else list[0] + sum(list[1..list.length])

squared_intersection = (cmap, ref_cmap) ->
    (Math.pow(count, 2) for trigram, count of cmap when ref_cmap[trigram])

generate_cmap = (text) ->
    cmap = {}
    for i in [0..text.length-3]
        trigram = text.substr(i, 3)
        if cmap.hasOwnProperty(trigram)
            cmap[trigram] += 1
        else
            cmap[trigram] = 1

    cmap

modulus = (cmap, ref_cmap) ->
    Math.sqrt(sum(squared_intersection(cmap, ref_cmap)))

inner_product = (cmap, ref_cmap) ->
    sum((count*ref_cmap[trigram]) for trigram, count of cmap when ref_cmap[trigram])

angle = (cmap, ref_cmap) ->
    inner_product(cmap, ref_cmap) / ( modulus(cmap, ref_cmap) * modulus(ref_cmap, ref_cmap) )

get_best_language_match = (ref_text, languages) ->
    ref_cmap = generate_cmap(ref_text)
    max_language = 'unknown'
    max_angle = -Number.MAX_VALUE

    for lang in languages
        cmap = generate_cmap(fs.readFileSync('../text/' + lang + '.txt', 'utf-8'))
        a = angle(cmap, ref_cmap)
        console.log('\t' + lang + ': ' + a)
        if a > max_angle
            max_language = lang
            max_angle = a

    max_language

analyse_languages = (languages) ->
    for language in languages
        console.log(language)
        matched = get_best_language_match(fs.readFileSync('../text/' + language + '-sample.txt', 'utf-8'), languages)
        if matched != language
            console.log("\tERROR: " + language + " != " + matched)
        else
            console.log("\tHIT: " + language + " == " + matched)

analyse_languages(['english', 'french', 'latin', 'spanish', 'portuguese', 'italian', 'german'])
