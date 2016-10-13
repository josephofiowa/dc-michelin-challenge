require 'torch'
require 'nn'
w2vutils = require 'w2vutils' -- via https://github.com/rotmanmi/word2vec.torch

-- Command line parameters
cmd = torch.CmdLine()
cmd:text()
cmd:text('Options for my NN')
cmd:option('-csv',"/media/alex/HD/Documents/Data/Yelp/to_classify.csv",'csv file')
cmd:option('-model',"model3.th",'prebuilt model')
cmd:option('-header',true,'csv has header')
-- etc...
cmd:text()
opt = cmd:parse(arg)

-- Data requirement: lua table with method size()
-- Method to read CSV
function string:splitAtCommas()
    local sep, values = ",", {}
    local pattern = string.format("([^%s]+)", sep)
    self:gsub(pattern, function(c) values[#values+1] = c end)
    return values
end

function string:splitAtSpaces()
    local sep, values = " ", {}
    local pattern = string.format("([^%s]+)", sep)
    self:gsub(pattern, function(c) values[#values+1] = c end)
    return values
end

function loadData(dataFile,header)
    local dataset = {}
    local length = 0
    local i = 1
    for line in io.lines(dataFile) do
        if header == true then
            header = false
        else
            local values = line:splitAtCommas()
            words = values[1]:splitAtSpaces() -- Split our review into words
            local x = torch.Tensor(300):zero() -- Initialize a 300x1 tensor of zeroes
            local wordCount = 0
            for j=1,#words,1 do
                vec = w2vutils:word2vec(words[j]) -- Add the word2vec value of each word to our tensor
                x = vec + x
                wordCount = wordCount + 1
            end
            x = x/wordCount -- Average the tensor by the word count, equivalent of doc2vec
            dataset[i] = {x}
            i = i + 1
        end
    end
    function dataset:size() return (i - 1) end -- the requirement mentioned
    function dataset:length() return 300 end
    return dataset
end

classifySet = loadData(opt.csv,opt.header)

-- Classify
mlp = torch.load(opt.model)

out = assert(io.open("./prediction_vectors.csv", "w"))

for i = 1, classifySet:size(), 1 do
    local x = classifySet[i][1]
    local predictions = mlp:forward(x)
    for j=1,predictions:size(1) do
        out:write(predictions[j])
        if j~=predictions:size(1) then
            out:write(",")
        end
    end
    out:write("\n")
end

out:close()
