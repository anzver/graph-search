import wx
import re
import cProfile


def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path


def parse(parsed_string):
    p = re.compile('[0-9]+')
    return p.findall(parsed_string)


def file_to_rib_list(file):
    rib_list = []
    loop_count = 0
    for line in file:
        rib = parse(line)
        if len(rib)== 2 :
            rib_list.append(rib)
            if rib[0] == rib[1] : loop_count +=1
    print 'loop count = ', loop_count
    return rib_list


def get_vertex_list(list_of_lists):
    vertex_list = []
    for sublist in list_of_lists:
        for element in sublist:
            if element not in vertex_list : vertex_list.append(element)
    return vertex_list


def wide_search(list_of_lists):
    print 'ribs count = ', len(list_of_lists)
    vertex_list = get_vertex_list(list_of_lists)
    print 'vertex count = ', len(vertex_list)
    vertex_map = dict.fromkeys(vertex_list,0)
    queue = []
    bucket_list = []
    while len(vertex_map) > 0:
        a = vertex_map.popitem()[0]
        queue.append(a)
        bucket = []
        while len(queue) > 0:
            a = queue.pop(0)
            bucket.append(a)
            for couple in list_of_lists:
                if couple[0] == a :
                    if (couple[1] not in queue) and (couple[1] not in bucket):
                        queue.append(couple[1])
                        del vertex_map[couple[1]]
                elif couple[1] == a :
                    if (couple[0] not in queue) and  (couple[0] not in bucket):
                        queue.append(couple[0])
                        del vertex_map[couple[0]]
        bucket_list.append(bucket)
    return bucket_list

def main(file):
    ribs = file_to_rib_list(file)
    graphs = wide_search(ribs)
    stat_table = {}
    for graph in graphs:
        key = len(graph)
        if key in stat_table: stat_table[key] += 1
        else: stat_table[key] = 1
    print(stat_table)


try:
    file=open(get_path('*.*'))
    cProfile.run('main(file)')
except IOError:
    print 'fuck'
