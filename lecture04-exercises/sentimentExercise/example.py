from pyspark import SparkConf, SparkContext
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()
from operator import add

# Read in negative and positive words list
positiveWords = ['absolutely','accepted','acclaimed','accomplish','accomplishment','achievement','action','active','admire','adorable','adventure','affirmative','affluent','agree','agreeable','amazing','angelic','appealing','approve','aptitude','attractive','awesome','beaming','beautiful','believe','beneficial','bliss','bountiful','bounty','brave','bravo','brilliant','bubbly','calm','celebrated','certain','champ','champion','charming','cheery','choice','classic','classical','clean','commend','composed','congratulation','constant','cool','courageous','creative','cute','dazzling','delight','delightful','distinguished','divine','earnest','easy','ecstatic','effective','effervescent','efficient','effortless','electrifying','elegant','enchanting','encouraging','endorsed','energetic','energized','engaging','enthusiastic','essential','esteemed','ethical','excellent','exciting','exquisite','fabulous','fair','familiar','famous','fantastic','favorable','fetching','fine','fitting','flourishing','fortunate','free','fresh','friendly','fun','funny','generous','genius','genuine','giving','glamorous','glowing','good','gorgeous','graceful','great','green','grin','growing','handsome','happy','harmonious','healing','healthy','hearty','heavenly','honest','honorable','honored','hug','idea','ideal','imaginative','imagine','impressive','independent','innovate','innovative','instant','instantaneous','instinctive','intellectual','intelligent','intuitive','inventive','jovial','joy','jubilant','keen','kind','knowing','knowledgeable','laugh','learned','legendary','light','lively','lovely','lucid','lucky','luminous','marvelous','masterful','meaningful','merit','meritorious','miraculous','motivating','moving','natural','nice','novel','now','nurturing','nutritious','okay','one','one-hundred percent','open','optimistic','paradise','perfect','phenomenal','pleasant','pleasurable','plentiful','poised','polished','popular','positive','powerful','prepared','pretty','principled','productive','progress','prominent','protected','proud','quality','quick','quiet','ready','reassuring','refined','refreshing','rejoice','reliable','remarkable','resounding','respected','restored','reward','rewarding','right','robust','safe','satisfactory','secure','seemly','simple','skilled','skillful','smile','soulful','sparkling','special','spirited','spiritual','stirring','stunning','stupendous','success','successful','sunny','super','superb','supporting','surprising','terrific','thorough','thrilling','thriving','tops','tranquil','transformative','transforming','trusting','truthful','unreal','unwavering','up','upbeat','upright','upstanding','valued','vibrant','victorious','victory','vigorous','virtuous','vital','vivacious','wealthy','welcome','well','whole','wholesome','willing','wonderful','wondrous','worthy','wow','yes','yummy','zeal','zealous']
negativeWords = ['abysmal','adverse','alarming','angry','annoy','anxious','apathy','appalling','atrocious','awful','bad','banal','barbed','belligerent','bemoan','beneath','boring','broken','callous','can\'t','clumsy','coarse','cold','cold-hearted','collapse','confused','contradictory','contrary','corrosive','corrupt','crazy','creepy','criminal','cruel','cry','cutting','damage','damaging','dastardly','dead','decaying','deformed','deny','deplorable','depressed','deprived','despicable','detrimental','dirty','disease','disgusting','disheveled','dishonest','dishonorable','dismal','distress','don\'t','dreadful','dreary','enraged','eroding','evil','fail','faulty','fear','feeble','fight','filthy','foul','frighten','frightful','gawky','ghastly','grave','greed','grim','grimace','gross','grotesque','gruesome','guilty','haggard','hard','hard-hearted','harmful','hate','hideous','homely','horrendous','horrible','hostile','hurt','hurtful','icky','ignorant','ignore','ill','immature','imperfect','impossible','inane','inelegant','infernal','injure','injurious','insane','insidious','insipid','jealous','junky','lose','lousy','lumpy','malicious','mean','menacing','messy','misshapen','missing','misunderstood','moan','moldy','monstrous','naive','nasty','naughty','negate','negative','never','no','nobody','nondescript','nonsense','not','noxious','objectionable','odious','offensive','old','oppressive','pain','perturb','pessimistic','petty','plain','poisonous','poor','prejudice','questionable','quirky','quit','reject','renege','repellant','reptilian','repugnant','repulsive','revenge','revolting','rocky','rotten','rude','ruthless','sad','savage','scare','scary','scream','severe','shocking','shoddy','sick','sickening','sinister','slimy','smelly','sobbing','sorry','spiteful','sticky','stinky','stormy','stressful','stuck','stupid','substandard','suspect','suspicious','tense','terrible','terrifying','threatening','ugly','undermine','unfair','unfavorable','unhappy','unhealthy','unjust','unlucky','unpleasant','unsatisfactory','unsightly','untoward','unwanted','unwelcome','unwholesome','unwieldy','unwise','upset','vice','vicious','vile','villainous','vindictive','wary','weary','wicked','woeful','worthless','wound','yell','yucky','zero']
    
print('Positive word count: ' + str(len(positiveWords)) + ', negative word count: ' + str(len(negativeWords)))

# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
conf = SparkConf().set('spark.executor.cores', 1).set('spark.cores.max',1).set('spark.executor.memory', '1g')
sc = SparkContext(master='spark://spark-master:7077', appName='myAppName', conf=conf)

# TODO: HINT! Remove select_words and define a function to return an integer based on the sentiment of the input word
select_words = lambda s : s[1] > 400

files = "hdfs://namenode:9000/stream-in/"
# Read in all files in the directory
txtFiles = sc.wholeTextFiles(files, 20)
# Take the content of the files and split them
all_word = txtFiles.flatMap(lambda s: s[1].split())

# TODO: HINT! Replace the implementation for word_map to run a function on each word, will return an RDD of just integers (basically a list of just integers)
# Change from list of words to list of (word, 1)
word_map = all_word.map(lambda s: (s, 1))

# TODO: HINT! Remove the rest of this code, and create and print the result by reducing the word_map with the operator "add"
# Merge values with equal keys
word_reduce = word_map.reduceByKey(lambda s, t: s+t)
# Filter using the defined lambda and sort by value
top_words = word_reduce.filter(select_words).sortBy(lambda s: s[1])
# Collect to a Python list and print
print(top_words.collect())
