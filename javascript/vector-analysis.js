var fs = require('fs');
var sys = require('sys');
var assert = require('assert');

function nGrams(size, lines) {
		var parts = {};
		for (i = 0; i < (lines.length - (size - 1)); i++) {
			  var ngram = lines.slice(i, i + size);
				if (parts[ngram] === undefined) {
						parts[ngram] = 1;
			  } else {
						parts[ngram] += 1;
				}
		}
		return parts;
}

function buildCorpora(languages) {
	  var corpora = {};
		languages.forEach(function (language) {
		    var path = '../text/' + language + '.txt';
			  var lines = fs.readFileSync(path).toString();
		    corpora[language] = nGrams(3, lines);
		});
		return corpora;
}

function modulus(first, second) {
		var result = 0;
		for (var ngram in first) {
				if (second[ngram] !== undefined) {
						result += Math.pow(first[ngram], 2);
				}
		}
		result = Math.pow(result, 0.5);
		return result;
}

function innerProduct(first, second) {
		var result = 0;
		for (var ngram in first) {
				if (second[ngram] !== undefined) {
					result += first[ngram] * second[ngram];
				}
		}
		return result;
}

function angleBetween(firstNGram, secondNGram) {
		return innerProduct(firstNGram, secondNGram) / (modulus(firstNGram, secondNGram) * modulus(secondNGram, secondNGram));
}

function analise(corpora, proposedLanguage) {
		var path = '../text/' + proposedLanguage + '-sample.txt';
		var text = fs.readFileSync(path).toString();
	  var ngrams = nGrams(3, text);
		var language = 'unknown';
		var maxAngle = -Number.MAX_VALUE;

		for (var currentLanguage in corpora) {
				var angle = angleBetween(ngrams, corpora[currentLanguage]);
			  if (angle > maxAngle) {
						maxAngle = angle;
						language = currentLanguage;
				}	
		}
		return language;
}

function verifyVectorAnalysis() {
    var languages = [ 'english', 'french', 'latin', 'portuguese', 'spanish', 'italian', 'german' ];
		var corpora = buildCorpora(languages);
		languages.forEach(function (language) {
		    assert.equal(analise(corpora, language), language);	
		});
    sys.puts('>> analysis successful!');
}

verifyVectorAnalysis();
