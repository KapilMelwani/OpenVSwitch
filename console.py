#!/usr/bin/env python
import sys
import ishell
import readline
import traceback
from ishell import logger

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Console(object):
    def __init__(self, prompt="Prompt", prompt_delim=">"):
        self.childs = {}
        self.prompt = prompt
        self.prompt_delim = prompt_delim
        self._exit = False

    def addChild(self, cmd):
        self.childs[cmd.name] = cmd
        return cmd

    def get_command(self, cmd_name):
        return self.childs[cmd_name]

    def is_child(self, cmd_name):
        return cmd_name in self.childs

    def completions(self, word=None):
        completions = [cmd.name + ' ' for cmd in self.childs.values()
                       if word is None or cmd.name.startswith(word)]
        return completions

    def walk(self, buf, state, run=False, full_line=None):
        # Current commands in line
        line = readline.get_line_buffer()
        line_commands = line.split()
        if run:
            line_commands = buf.split()
        logger.debug("Line=>%s" % line_commands)

        if not line and not buf and not run:
            completions = self.completions() + [None]
            return completions[state]

        # Traversing current command
        for cmd_name in line_commands:
            if self.is_child(cmd_name):
                logger.debug("Found existing command=>%s" % cmd_name)
                cmd = self.get_command(cmd_name)
                return cmd.complete(line_commands[1:], buf, state, run, full_line)

        if run:
            #print "Unknown Command: %s" % buf
            print Colors.FAIL + "[ERROR] " + Colors.ENDC + "%s: command not found" % buf
            return
            #self.print_childs_help()
        # Needing completion
        logger.debug('buffer=> %s, state=>%s' % (buf, state))
        tokens = buf.split()
        logger.debug('tokens=>%s' % tokens)

        # Nothing was provided, running root completion
        completions = self.completions(tokens[0])
        completions += [None]
        logger.debug('completions=>%s' % completions)
        logger.debug('END COMPLETE')
        return completions[state]


    def walk_and_run(self, command):
        self.walk(command, 0, run=True, full_line=command)

    # def print_childs_help(self):
    #     print "Help:"
    #     for command_name in sorted(self.childs.keys()):
    #         print "%15s - %s" % (command_name, self.childs[command_name].help)
    #     print

    def loop(self):
        previous_completer = readline.get_completer()
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.walk)
        prompt = self.prompt + self.prompt_delim
        if not ishell._current_prompt:
            previous_prompt = prompt
        else:
            previous_prompt = ishell._current_prompt
        ishell._current_prompt = prompt
        while 1:
            try:
                sys.stdout.write("\r")
                if self._exit:
                    break
                sys.stdout.write("\033[K")
                input_ = raw_input(prompt + " ")
                if not input_.strip():
                    #self.print_childs_help()
                    continue
                elif input_ in ('quit', 'bye'):
                    break
                else:
                    self.walk_and_run(input_)
            except (KeyboardInterrupt, EOFError):
                print "bye"
                break

            except Exception:
                print traceback.format_exc()
                sys.exit(1)

        ishell._current_prompt = previous_prompt
        readline.set_completer(previous_completer)
