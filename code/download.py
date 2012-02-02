"""%prog [-d|--dryrun] [-f|--formats `formats`] [-c|--categories `categories`] [-u|--update] [-l|--list]

    Script to download Khan Academy videos for offline use with option to update an existing download.  Uses archive.org whenever possible to grab mp4 or ogg formats but has fallback to flv from Khan official site.
"""
import sys, urllib, os, traceback
import logging
from optparse import OptionParser
from video_mapping import video_mapping
log = logging.getLogger(__name__)

FORMATS = ['.mp4','.ogg','.flv']
ARCHIVE_URL = "http://www.archive.org/download/KhanAcademy"
        
def urlretrieve(urlfile, fpath):
    chunk = 2**20
    f = open(fpath, "wb")
    while 1:
        data = urlfile.read(chunk)
        if data[:6] == "<html>":
            raise Exception("video not available")
        if not data:
            break
        f.write(data)
        print "*",
    print
    
def download_videos(categories, formats, flash=False, dryrun=False): 
    for category in categories:
        videos = video_mapping[category]
        folder = "videos/" + category
        for format in formats:       
            if not os.path.exists(folder):
                os.mkdir(folder)
    
            for title, youtube_id, readable_id in videos:
                filepath = folder + "/" + readable_id + format
                if os.path.exists(filepath) and os.stat(filepath).st_size > 0:
                    print "%s already downloaded" % readable_id
                else:
                    # first try archive.org, download speed is faster  
                    try:
                        # sample url: http://www.archive.org/download/KA-converted-rAof9Ld5sOg/rAof9Ld5sOg.mp4
                        if format == '.mp4':
                            url = ARCHIVE_URL + "_" + category + "/" + readable_id + "_512kb" +  format
                        else:
                            url = ARCHIVE_URL + "_" + category + "/" + readable_id + format
                        urlfile = urllib.urlopen(url)
                        if dryrun:
                            print "DRYRUN: To be downloaded from archive.org: ", url
                            # TODO print out the file type of what's at the url
                        else:
                            # TODO confirm url is a video and not html here
                            print "Downloading: ", url
                            urlretrieve(urlfile, filepath)
                            if os.stat(filepath).st_size == 0:
                                os.remove(filepath)
                                print "Removing empty file: ", filepath
                    except:        
                        traceback.print_exc()
                        # We're not going to download from YouTube as the exception handling
                        #os.system('python ../youtube-dl.py -f 34 -icw -o "' + folder + '/' + readable_id + '.flv" http://www.youtube.com/watch?v=' + youtube_id)
                    

if __name__ == '__main__':
    parser = OptionParser(__doc__)
    parser.set_defaults(
            formats='.mp4',
            update=False,
            dryrun=False,
            flash_fallback=True,
            list_categories=False,
            categories='Geometry',
            )
    # update is not implemented yet
    parser.add_option("-u", "--update", dest="update", action="store_true",
            help="don't bother downloading the entire video_mapping, check rss for new videos and download")
    parser.add_option("-d", "--dryrun", dest="dryrun", action="store_true",
            help="just output what will be downloaded, without downloading anything")
    parser.add_option("-f", "--formats", dest="formats",
            help="specify the preferred formats to download videos in")
    parser.add_option("-l", "--list", dest="list_categories", action="store_true",
            help="list the available categories which contain videos")
    parser.add_option("-c", "--categories", dest="categories",
            help="specify the categories to download videos for (comma separated list)")
    parser.add_option("--flash-fallback", dest="flash_fallback", action="store_true",
            help="if format(s) specified not available, download flash version if exists")

    options, args = parser.parse_args()
    
    user_formats = options.formats.split(',')
    formats = [f for f in user_formats if f in FORMATS]
    log.info("Formats: %s " % formats)
        
    if options.list_categories:
        print "Available categories: "
        for k in video_mapping.keys():
            print 'http://www.archive.org/download/KhanAcademy_%s' % k
        sys.exit(1)

    if options.categories == 'all':
        categories = video_mapping.keys()
    else:
        user_categories = options.categories.split(',')
        categories = [c for c in user_categories if c in video_mapping.keys()]
        log.info("Categories: %s" % categories)

    download_videos(categories, formats, options.flash_fallback, options.dryrun)