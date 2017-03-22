import logging
from copy import deepcopy
import pprint

from falafel.console.custom_logging import print_console

logger = logging.getLogger(__name__)


class Formatter(object):
    def __init__(self, args):
        self.screen_height, self.screen_width = get_screen_width()
        self.screen_width = args.max_width if args.max_width else self.screen_width
        self.list_missing = args.list_missing
        self.list_plugins = args.list_plugins

    def display_list(self, items):
        if not items:
            print_console("")
            return

        col_size = max(map(len, items))
        col_cnt = self.screen_width / col_size
        col_size = col_size + ((self.screen_width % col_size) / col_cnt)

        sorted_items = sorted(items)
        chunk_iter = (sorted_items[i:i + col_cnt] for i in xrange(0, len(sorted_items), col_cnt))
        for chunks in chunk_iter:
            row = ''.join(item.ljust(col_size) for item in chunks)
            print_console(row)

        print_console("")

    def heading(self, text):
        print_console("\n" + "  {0}  ".format(text).center(self.screen_width, "="))

    def hanging_indent(self, line, indent_size, word_wrap=True):
        line = line.rstrip()
        if len(line) <= self.screen_width:
            return line

        def do_wrap(l, i):
            if l.find("\n") >= 0 and l.find("\n") < i:
                return l.find("\n")
            elif word_wrap and i < len(l):
                rightmost_space = l.rfind(" ", 0, i)
                return rightmost_space if rightmost_space > -1 else i
            else:
                return i

        lines = [line[0:do_wrap(line, self.screen_width)]]
        line = line[do_wrap(line, self.screen_width):]
        while line:
            line = line.strip("\n")
            end_idx = min(len(line), do_wrap(line, self.screen_width - indent_size))
            lines.append(" " * indent_size + line[:end_idx])
            line = line[end_idx:]
        return "\n".join(lines)

    def format_value(self, value, indent_size):
        pp = pprint.PrettyPrinter(width=self.screen_width - indent_size)

        ret_val = value
        if isinstance(value, list):
            if (any(t for t in (dict, tuple) if t in map(type, value)) or
                    not value):
                ret_val = pp.pformat(value)
            else:
                ret_val = ", ".join(map(str, value)).rstrip()
        elif isinstance(value, basestring):
            ret_val = '"{}"'.format(value)
        elif isinstance(value, dict):
            ret_val = pp.pformat(value)

        return ret_val

    def display_dict_of_strings(self, d, sort=False, margin=0, word_wrap=True):
        key_field_size = max(map(len, d.keys())) + 1
        indent_size = margin + key_field_size + 2
        display_fmt = "{}{}: {}"
        d_items = sorted(d.iteritems()) if sort else d.iteritems()
        for key, value in d_items:
            value = self.format_value(value, indent_size)
            line = display_fmt.format(
                ' ' * margin,
                key.ljust(key_field_size),
                value)
            print_console(self.hanging_indent(line, indent_size, word_wrap))

    def display_results(self, results, stats):
        result_count = 0
        for module, result in sorted(results.iteritems()):
            if result:
                print_console(module + ":")
                self.display_dict_of_strings(result, sort=True, margin=4, word_wrap=False)
                print_console("-" * self.screen_width)
                result_count += 1

        print_console("Result: {0} issues found; {1} rules run; {2} skipped\n".
                      format(result_count, len(results), stats["skips"]["count"]))
        logger.info("Mapper : {0} executed; {1} failed".
                    format(stats["mapper"]["count"], stats["mapper"]["fail"]))
        logger.info("Reducer: {0} executed; {1} failed".
                    format(stats["reducer"]["count"], stats["reducer"]["fail"]))

    def display_system_data(self, system_data):
        d = {key: system_data[key] for key in system_data.keys() if key != "metadata"}
        d.update(system_data.get("metadata", {}))
        self.display_dict_of_strings(d)

    def display_missing_requirement(self, skips):
        for skip in skips:
            s = deepcopy(skip)
            del s["reason"]
            self.display_dict_of_strings(s)
            print_console("")

    def format_results(self, system, skips, reports, archives, stats):
        if archives:
            self.heading("Multi Archive (%s nested archives)" % len(archives))
        items = {}

        for module, output in list(reports):
            items[module] = output

        if not items:
            print_console("No plugins executed")
            return
        if self.list_plugins:
            self.heading("Executed modules")
            self.display_list(items.keys())
        if self.list_missing:
            if skips:
                self.heading("Missing requirements")
                self.display_missing_requirement(skips)
            else:
                print_console("No files were missing")
        self.heading("System Data")
        self.display_system_data(system)
        self.heading("Results")
        self.display_results(items, stats)
        if archives:
            self.list_plugins = False
            for each in archives:
                self.format_results(each.get("system", {}),
                                    each.get("skips", []),
                                    each.get("reports", []),
                                    None,
                                    each.get("stats", {}))


def get_screen_width():
    try:
        import fcntl
        import termios
        import struct
        screen_height, screen_width = struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, 'neat'))
    except:
        return 24, 80
    else:
        return screen_height, screen_width
