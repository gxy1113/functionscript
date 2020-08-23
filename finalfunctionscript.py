import os
import sys
import time
from collections import defaultdict
packages = {'libelfin','target_libtiff','graphicsmagick-1.3.35','libpng','binutils','lava-m',
'xpdf','libjson','jhead','libjpeg_turbo','ffjpeg','flvmeta','mupdf','lame'} 
special_packages = {'libelfin','target_libtiff','binutils','lava-m','xpdf','libjpeg_turbo'} #下面有子程序的程序集，例如binutils
notice_packages = {'target_libtiff','graphicsmagick-1.3.35','binutils','lava-m','ffjpeg','xpdf','libjson','jhead','lame','mupdf','libjpeg_turbo'}
parameter_packages = {'libjson','jhead','ffjpeg'}
normal_packages = packages-special_packages-parameter_packages
package_list = defaultdict(list)
package_list['all1'] = ['libjson','jhead','target_libtiff']
package_list['all2'] = ['xpdf','binutils','ffjpeg']
package_list['all3'] = ['lava-m','libelfin']
package_list['all4'] = ['flvmeta','libpng']

def dir_select(target_prog,target_package): #输入、输出、目标程序的相对路径
    if target_package == 'libelfin':
        input_seed = 'others/elf2/'
        prog_list = target_prog.split('-')
        output_dir = "fuzz_out_libelfin_"+prog_list[0]+"_"+prog_list[1]+"/"
        prog_dir = "target_libelfin/libelfin/examples/"+target_prog
    elif target_package == 'libjpeg_turbo':
        input_seed = 'images/jpeg/'
        prog_list = target_prog.split('-')
        output_dir = 'fuzz_out_' + prog_list[0] + "_" + prog_list[1] + "/"
        prog_dir = 'target_libjpeg_turbo/install/bin/' + prog_list[0]
    elif target_package == "flvmeta":
        input_seed = 'multimedia/flv/'
        output_dir = 'fuzz_out_flvmeta/'
        prog_dir = 'target_flvmeta/install/bin/flvmeta'
    elif target_package == "mupdf": #notice
        input_seed = 'others/pdf/'
        output_dir = 'fuzz_out_mupdf_mutool_draw'
        prog_dir = 'target_mupdf/mupdf-1.17.0-source/build/release/mutool'
    elif target_package == "target_libtiff":
        input_seed = 'images/tiff/'    
        output_dir = 'fuzz_out_libtiff_'+target_prog
        if target_prog == 'tiff2rgb':
            prog_dir = 'target_libtiff/install/bin/'+target_prog
        else:
            prog_dir = 'target_libtiff/install/bin/'+target_prog
    elif target_package == "target_libzip":
        input_seed = 'archives/common/bzip2/'
        output_dir = 'fuzz_out_bzip2_bzcat/'
        prog_dir = 'target_bzip2/install/bin/bzcat'
    elif target_package == "manalyzer":  #notice
        input_seed = 'others/elf/'
        output_dir = 'fuzz_out_manafuzz'
        prog_dir = 'target_manafuzz/manafuzz/manafuzz'
    elif target_package == "libav": #notice
        input_seed = 'multimedia/h264/'
        output_dir = 'fuzz_out_libav_' + target_prog
        prog_dir = 'target_libav/install/bin/' + target_prog
    elif target_package == "graphicsmagick-1.3.35": #notice
        input_seed = 'images/png/'
        output_dir = 'fuzz_out_graphicsmagick'
        prog_dir = 'target_graphicsmagick/install/bin/gm'
    elif target_package == "libpng":
        input_seed = 'images/png/'
        output_dir = 'fuzz_out_libpng'
        prog_dir = 'target_libpng/readpng-file-input'
    elif target_package == "tcpdump": #notice
        input_seed = 'others/pcap/'
        output_dir = 'fuzz_out_tcpdump'
        prog_dir = 'target_tcpdump/install/sbin/tcpdump'
    elif target_package == "binutils":
        input_seed = 'others/elf/'
        output_dir = 'fuzz_out_binutils_'+target_prog
        prog_dir = 'target_binutils/install/bin/'+target_prog
    elif target_package == "lava-m": 
        prog_list = target_package.split('-')
        target_package = prog_list[0] + '_' + prog_list[1]
        output_dir = 'fuzz_out_lavam_' + target_prog
        prog_dir = 'lava_corpus/LAVA-M/' + target_prog + '/coreutils-8.24-lava-safe/lava-install/bin/' + target_prog
        if target_prog == "base64":
            input_seed = 'lava_m/lava_m_base64/'
        elif target_prog == "md5sum":
            input_seed = 'lava_m/lava_m_md5sum/'
        elif target_prog == "uniq":
            input_seed = 'lava_m/lava_m_uniq/'
        elif target_prog == "who":
            input_seed = 'lava_m/lava_m_who/'
    elif target_package == "ffjpeg": # parameter d or e
        if target_prog == 'd':
            input_seed = 'images/jpeg/'
        elif target_prog == 'e':
            input_seed = 'images/bmp/'
        output_dir = 'fuzz_out_ffjpeg_' + target_prog
        prog_dir = 'target_ffjpeg/ffjpeg/src/ffjpeg'
    elif target_package == "xpdf": #notice
        input_seed = 'others/pdf/'
        output_dir = 'fuzz_out_xpdf_' + target_prog
        prog_dir = 'target_xpdf/install/bin/' + target_prog
    elif target_package == "libjson": #notice
        input_seed = 'others/json/'
        if target_prog == 'tree':
            output_dir = 'fuzz_out_libjson_tree'
        else:
            output_dir = 'fuzz_out_libjson'
        prog_dir = 'target_libjson/libjson/jsonlint'
    elif target_package == 'jpeg2png': #notice
        input_seed = 'images/jpeg/'
        output_dir = 'fuzz_out_jpeg2png'
        prog_dir = 'target_jpeg2png/jpeg2png/jpeg2png'
    elif target_package == 'jhead': #notice
        input_seed = 'images/jpeg/'
        output_dir = 'fuzz_out_jhead_' + target_prog
        prog_dir = 'target_jhead/install/jhead'
    elif target_package == "jasper":
        input_seed = 'sum_images/'
        output_dir = 'fuzz_out_jasper_' + target_prog
        prog_dir = 'target_jasper/install/bin/' + target_prog
    elif target_package == "lame":
        input_seed = 'multimedia/wav/'
        output_dir = 'fuzz_out_lame'
        prog_dir = 'target_lame/install/bin/lame'
    else:
        input_seed = 'non_exist'
    return input_seed,output_dir,prog_dir
def package_input(packages): #程序集名称输入，例如binutils
    print("please enter the name of package")
    target_package = input()
    if target_package in packages:
        return target_package
    elif target_package == 'all1' or target_package == 'all2' or target_package == 'all3' or target_package == 'all4' or target_package == 'all7':
        return target_package
    else:
        print('This specific program has not been documented in the script, please update the script and try again later')
def prog_input(target_package): #子程序名称输入，例如objdump；或者特殊参数的输入例如libjson的tree参数
    if target_package in special_packages:
        print("please enter the name of paragram")
        target_prog = input()
        return target_prog
    elif target_package == "libjson" or target_package == "jhead" or target_package == 'ffjpeg':
        print("please enter the parameter:")
        target_prog = input()
        return target_prog
def porg_set(package):
    if package == 'libelfin':
        progs = {'dump-lines','dump-tree','dump-sections','dump-segments','dump-syms'}
    elif package == 'target_libtiff':
        progs = {'tiffinfo','tiff2rgba','tiffdump','tiff2ps','tiff2pdf'}
    elif package == 'libav':
        progs = {'avconv'}
    elif package == 'binutils':
        progs = {'objdump','nm','size','readelf'}
    elif package == 'lava-m':
        progs = {'base64','md5sum','uniq','who'}
    elif package == 'xpdf':
        progs = {'pdfimages','pdftotext'}
    elif package == 'libjson':
        progs = {'tree','non'}
    elif package == 'jhead':
        progs = {'purejpg','mkexif','autorot'}
    elif package == 'jasper':
        progs = {'jasper','imginfo'}
    elif package == 'ffjpeg':
        progs = {'d','e'}
    elif package == 'libjpeg_turbo':
        progs = {'jpegtran-progressive','jpegtran-arithmetic','jpegtran-optimize','jpegtran-pnm','djpeg-bmp','djpeg-gif'}
    return progs
def afl_command(input_seed,output_dir,prog_dir,target_prog,target_package,afl_origin_title):
    if target_package not in notice_packages:
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@'
    elif target_package == 'mupdf':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' draw @@'
    elif target_package == 'libjpeg_turbo':
        prog_list = target_prog.split('-')
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -m500 -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir + ' -' + prog_list[1] + ' @@'
    elif target_package == 'target_libtiff':
        if target_prog == 'tiff2rgb':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@ ' + afl_origin_title +'testtiff2rgb'
        else:
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@'
    elif target_package == 'manalyzer':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -m500 -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -t100 -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@'    
    elif target_package == 'libav':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -m500 -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -i @@'
    elif target_package == 'graphicsmagick-1.3.35':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -m500 -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' convert @@ ' + afl_origin_title + 'test.pdf'
    elif target_package == 'tcpdump':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -nr @@'
    elif target_package == 'binutils':
        if target_prog == 'objdump':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -d @@'
        elif target_prog == 'readelf':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -a @@'
        else:
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@'
    elif target_package == 'lava-m':
        if target_prog == 'base64':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -d @@'
        elif target_prog == 'md5sum':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -c @@'
        else:
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@'
    elif target_package == 'ffjpeg':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -' + target_prog + ' @@'
    elif target_package == 'xpdf':
        if target_prog == 'pdfimages' or target_prog == 'pdftopng':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@ /dev/null'
        else:
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@'
    elif target_package == 'libjson':
        if target_prog == 'tree':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' ' + afl_origin_title + '../../../target_progs/' + prog_dir +' --tree @@'
        else:
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@'
    elif target_package == 'jpeg2png':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -m500 -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@ /dev/null'
    elif target_package == 'jhead':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir + ' -' + target_prog + ' @@'
    elif target_package == 'jasper':
        if target_prog == 'jasper':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' --input @@ --output /dev/null --output-format jp2'
        elif target_prog == 'imginfo':
            afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' -f @@'
    elif target_package == 'lame':
        afl_origin_dir = './' + afl_origin_title + 'afl-fuzz -m500 -i ' + afl_origin_title + 'testcases/' + input_seed + ' -o ' + afl_origin_title + '../fuzz_out/' + output_dir + ' -- ' + afl_origin_title + '../../../target_progs/' + prog_dir +' @@ /dev/null'
    return afl_origin_dir    
def function210_command(input_seed,output_dir,prog_dir,target_prog,target_package,brige_title):
    if target_package == 'lava-m':
        mkdir_command = 'mkdir -p ' + brige_title + '../fuzz_out/' + output_dir
        afl_brige_command = './' + brige_title + 'brige.sh -f ' + brige_title + '../fuzz_out/' + output_dir + ' -t ' + brige_title + '../../../' + prog_dir
    else:
        mkdir_command = 'mkdir -p ' + brige_title + '../fuzz_out/' + output_dir
        afl_brige_command = './' + brige_title + 'brige.sh -f ' + brige_title + '../fuzz_out/' + output_dir + ' -t ' + brige_title + '../../../target_progs/' + prog_dir
    return mkdir_command,afl_brige_command
def remove_function(dir_remove,afl_function_title,afl_fast_title,afl_fair_title,afl_origin_title,output_dir):
    if dir_remove == 'yes':
        afl_dir_remove = 'rm -rf ' + afl_origin_title + '../fuzz_out/' + output_dir
        fast_dir_remove = 'rm -rf ' + afl_fast_title + '../fuzz_out/' + output_dir
        fair_dir_remove = 'rm -rf ' + afl_fair_title + '../fuzz_out/' + output_dir
        function_dir_remove = 'rm -rf ' + afl_function_title + '../fuzz_out/' + output_dir
        os.system('%s' %(afl_dir_remove))
        os.system('%s' %(fast_dir_remove))
        os.system('%s' %(fair_dir_remove))
        os.system('%s' %(function_dir_remove))
        return afl_dir_remove
if __name__ == "__main__":
    print("remove or not")
    dir_remove = input()
    target_package = package_input(packages)
    afl_origin_title = '../Fuzz/origin/afl-2.52b/'
    afl_fast_title = '../Fuzz/fast/aflfast/'
    afl_fair_title = '../Fuzz/fair/afl-rb/'
    afl_brige_title = '../Fuzz/function/scripts/'
    afl_function_title = '../Fuzz/function/afl-2.52b/'
    if  target_package == 'all1' or target_package == 'all2' or target_package == 'all3':
        package_phase = package_list[target_package]
        for package in package_phase:
            progs = porg_set(package)
            for prog in progs:
                input_seed,output_dir,prog_dir = dir_select(prog,package)
                if dir_remove == 'yes':
                    afl_dir_remove = remove_function(dir_remove,afl_function_title,afl_fast_title,afl_fair_title,afl_origin_title,output_dir)
                afl_origin_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_origin_title)
                afl_fast_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_fast_title)
                afl_fair_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_fair_title)
                mkdir_command,afl_brige_command = function210_command(input_seed,output_dir,prog_dir,prog,package,afl_brige_title)
                afl_function_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_function_title)
                intermediary_list = afl_fast_command.split(' ',1)
                afl_fast_command = intermediary_list[0] + ' -p fast ' + intermediary_list[1]
                os.system("screen -dmS %s-%s-origin %s" %(prog,package,afl_origin_command))
                os.system("screen -dmS %s-%s-fast %s" %(prog,package,afl_fast_command))
                os.system('screen -dmS %s-%s-fair %s' %(prog,package,afl_fair_command))
                os.system("%s" %(mkdir_command))
                os.system('screen -dmS %s-%s-brige %s' %(prog,package,afl_brige_command))
                time.sleep(2)
                os.system('screen -dmS %s-%s-function %s' %(prog,package,afl_function_command))
    elif target_package == 'all4':
        package_phase = package_list[target_package]
        for package in normal_packages:
            prog=''
            input_seed,output_dir,prog_dir = dir_select(prog,package)
            if dir_remove == 'yes':
                afl_dir_remove = remove_function(dir_remove,afl_function_title,afl_fast_title,afl_fair_title,afl_origin_title,output_dir)
            afl_origin_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_origin_title)
            afl_fast_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_fast_title)
            afl_fair_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_fair_title)
            mkdir_command,afl_brige_command = function210_command(input_seed,output_dir,prog_dir,prog,package,afl_brige_title)
            afl_function_command = afl_command(input_seed,output_dir,prog_dir,prog,package,afl_function_title)
            intermediary_list = afl_fast_command.split(' ',1)
            afl_fast_command = intermediary_list[0] + ' -p fast ' + intermediary_list[1]
            os.system("screen -dmS %s-%s-origin %s" %(prog,package,afl_origin_command))
            os.system("screen -dmS %s-%s-fast %s" %(prog,package,afl_fast_command))
            os.system('screen -dmS %s-%s-fair %s' %(prog,package,afl_fair_command))
            os.system("%s" %(mkdir_command))
            os.system('screen -dmS %s-%s-brige %s' %(prog,package,afl_brige_command))
            time.sleep(2)
            os.system('screen -dmS %s-%s-function %s' %(prog,package,afl_function_command))
    elif target_package in packages:
        target_prog = prog_input(target_package)
        input_seed,output_dir,prog_dir = dir_select(target_prog,target_package)
        if dir_remove == 'yes':
            afl_dir_remove = remove_function(dir_remove,afl_function_title,afl_fast_title,afl_fair_title,afl_origin_title,output_dir)
        afl_origin_command = afl_command(input_seed,output_dir,prog_dir,target_prog,target_package,afl_origin_title)
        afl_fast_command = afl_command(input_seed,output_dir,prog_dir,target_prog,target_package,afl_fast_title)
        afl_fair_command = afl_command(input_seed,output_dir,prog_dir,target_prog,target_package,afl_fair_title)
        mkdir_command,afl_brige_command = function210_command(input_seed,output_dir,prog_dir,target_prog,target_package,afl_brige_title)
        afl_function_command = afl_command(input_seed,output_dir,prog_dir,target_prog,target_package,afl_function_title)
        intermediary_list = afl_fast_command.split(' ',1)
        afl_fast_command = intermediary_list[0] + ' -p fast ' + intermediary_list[1]
        print(afl_origin_command)
        print(afl_fast_command)
        print(afl_fair_command)
        print(afl_function_command)
        print(afl_brige_command)
        os.system("screen -dmS %s-%s-origin %s" %(target_prog,target_package,afl_origin_command))
        os.system("screen -dmS %s-%s-fast %s" %(target_prog,target_package,afl_fast_command))
        os.system('screen -dmS %s-%s-fair %s' %(target_prog,target_package,afl_fair_command))
        os.system("%s" %(mkdir_command))
        os.system('screen -dmS %s-%s-brige %s' %(target_prog,target_package,afl_brige_command))
        time.sleep(3)
        os.system('screen -dmS %s-%s-function %s' %(target_prog,target_package,afl_function_command))
        os.system('export TERM=xterm-xfree86')
