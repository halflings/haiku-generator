import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic


class WordNetUtil:
    brown_ic = wordnet_ic.ic('ic-brown.dat')
    @staticmethod
    def get_related_word_list(word, posTag='ALL'):
        result_list = [];
        res = [];
        for ss in (wn.synsets(word)):
            name = ss.name().partition('.')[0].replace("_", " ");
            result_list.extend(nltk.pos_tag([name]));
            result_list.extend(WordNetUtil.__processString(ss.definition()));
            for ex in ss.examples():
                result_list.extend(WordNetUtil.__processString(ex));
            
            for h in ss.hypernyms():
                hyper = h.name().partition('.')[0].replace("_", " ");
                result_list.extend(nltk.pos_tag([hyper]));
                result_list.extend(WordNetUtil.__processString(h.definition()));
            
            for h in ss.hyponyms():
                hypo = h.name().partition('.')[0].replace("_", " ");
                result_list.extend(nltk.pos_tag([hypo]));
                result_list.extend(WordNetUtil.__processString(h.definition()));

            for lem in ss.lemmas():
                name = lem.name().replace("_", " ");
                result_list.extend(nltk.pos_tag([name]));


        seen = set();
        resSet = set();
        for item in result_list:
            w = wn.morphy(item[0]);
            if w is None:
                continue;
            if w not in seen:
                seen.add(w);
                resSet.add((w, item[1]));       

        
        #prelimList = list(resSet);
        #inWordSS = wn.synsets(word)[0];
        #result_list = [];
        #for w in prelimList:
            #ss = wn.synsets(w[0])[0];
            #simScore = inWordSS.res_similarity(ss, WordNetUtil.brown_ic);
            #result_list.extend((w[0], w[1], simScore));

        result_list = list(resSet);
        
        if(posTag == 'ALL'):
            return result_list;

        for w in result_list:
            #print w;
            if(w[1].startswith(posTag)):
                res.append((w[0], w[1]));

        return res;

    @staticmethod
    def __processString(str_):
        tokens = nltk.word_tokenize(str_);
        tagged = nltk.pos_tag(tokens);
        return tagged;