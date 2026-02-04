import os

def parse_line(line: str, delim: str):
    split_line = line.split(delim)
    if(len(split_line) < 4):
        return (("", 0, 0), [])
    question = split_line[0], int(split_line[1]), int(split_line[2])
     
    answers = [split_line[i].strip('\n') for i in range(3, len(split_line))]

    return question, answers
def parse_txt_file(fpath: str, delim: str):
    assert(os.path.exists(fpath))
    lines =[]
    with open(fpath, 'r+') as f:
        lines = f.readlines()

    return [parse_line(line, delim) for line in lines]
        

if __name__ == "__main__":
    file_path = "Ch06-2947-example.txt"
    print(parse_txt_file(file_path, ";"))
        
    

    





