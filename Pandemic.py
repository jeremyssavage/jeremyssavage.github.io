import os,pickle
import matplotlib.pyplot as plt
from numpy import mean

role_list = ["contingency planner", "dispatcher", "medic", "operations expert", "quarantine specialist", "researcher", "scientist"]


class cSession:
    # A session is an individual play.
    # The information to be stored should be submitted at game end.

    def __init__(self):
        self.players = 0
        self.roles = ["","","",""]
        self.result = "?"
        self.stats = [-1, -1,-1,-1,-1, -1,-1,-1]
        
    def set_players(self, num_players):
        if num_players.isdigit() and 2 <= int(num_players) <= 4:
            self.players = int(num_players)
            return 0
        else:
            print("ERROR: invalid input")
            return 2

    def get_players(self):
        return self.players

    def set_role(self, role_num, role_in):
        # Check that the role number is leq than the number of players.
        if role_num < 1 or self.players < role_num:
            print("CODE ERROR: invalid role_num")
            sys.exit()

        # Check that role input is non-empty.
        if role_in == "":
            print("ERROR: invalid input")
            return 2

        # Check that role input matches a valid role, and "autocomplete".
        role_out = ""
        for role in role_list:
            if role_in.lower() == role[0:len(role_in)]:
                role_out = role
        if role_out == "":
            print("ERROR: invalid input")
            return 2

        # Check if the role has already been entered for this session.
        for role in self.roles[0:role_num-1]:
            if role.lower() == role_out:
                print("ERROR: role already entered for this session.")
                return 2

        # Store the role and exit.
        self.roles[role_num-1] = role_out
        return 0

    def get_role_by_number(self, role_number):
        if 1 <= role_number <= self.players:
            return self.roles[role_number-1]
        else:
            print("CODE ERROR: requested role out of bounds")

    def get_role_by_name(self, role_name):
        role_count = self.roles.count(role_name)
        if role_count == 0:
            return 0
        elif role_count == 1:
            return self.roles.index(role_name)+1
        else:
            print("CODE ERROR: multiple identical roles found in self.roles")
            sys.exit()

    def set_result(self, result_in):
        # Result is either a win or loss.
        error = 0
        if result_in != "":
            result_out = result_in[0].lower()
        
        if result_out == "w" or result_out == "l":
            self.result = result_out
            return 0
        else:
            error = 1

        if error == 1:
            print("ERROR: invalid input")

    def get_result(self):
        return self.result

    def set_stat(self, stat_id, stat_in):
        # The "stats" are the game values along the top bar of the app.
        # Number of player cards, disease cubes, research stations, outbreak and infection levels.
        
        if stat_in.isdigit():
            stat_int = int(stat_in)
        else:
            print("ERROR: invalid input")
            return 2
        
        error = 0
        # 48 city cards + 5 event cards + 6 epidemic cards = 59 player cards
        # 2p: 4 cards per player = 51 cards in deck: 12 12 12 12 12 12 12 12 12 12 12 12 12 = 13/13 turns
        # 3p: 3 cards per player = 50 cards in deck: 123 123 123 123 123 123 123 123 12 = 9/9/8 turns
        # 4p: 2 cards per player = 51 cards in deck: 1234 1234 1234 1234 1234 1234 12 = 7/7/6/6 turns
        if stat_id == 0:   # Player cards.
            if stat_int < 0 or 51 < stat_int or (stat_int>0 and stat_int%2==self.players%2):
                error = 2
        elif 1 <= stat_id <=4:   # Disease cubes (blue, yellow, black, red).
            if stat_int < 0 or 24 < stat_int:
                error = 2
        elif stat_id == 5:   # Research stations.
            if stat_int < 0 or 5 < stat_int:
                error = 2
        elif stat_id == 6:   # Outbreaks.
            if stat_int < 0 or 8 < stat_int:
                error = 2
        elif stat_id == 7:   # Infection level.
            if stat_int < 2 or 4 < stat_int:
                error = 2
        else:
            print("CODE ERROR: invalid stat_id")
            sys.exit()
        if error == 2:
            print("ERROR: invalid input")
            return 2

        self.stats[stat_id] = stat_int
        return 0

    def get_player_cards(self):
        return self.stats[0]

    def get_cubes_blue(self):
        return self.stats[1]

    def get_cubes_yellow(self):
        return self.stats[2]

    def get_cubes_black(self):
        return self.stats[3]

    def get_cubes_red(self):
        return self.stats[4]

    def get_cubes_total(self):
        return sum(self.stats[1:5])

    def get_research_stations(self):
        return self.stats[5]

    def get_outbreaks(self):
        return self.stats[6]

    def get_infection_levels(self):
        return self.stats[7]

    def print_session(self):
        output = ""
        if self.roles[0] <> "":
            output += "{:>6s}".format(self.roles[0][0:3].title())
        if self.roles[1] <> "":
            output += "{:>4s}".format(self.roles[1][0:3].title())
        if self.roles[2] <> "":
            output += "{:>4s}".format(self.roles[2][0:3].title())
        if self.roles[3] <> "":
            output += "{:>4s}".format(self.roles[3][0:3].title())

        if self.result == "w":
            output += "{:>4s}".format("W")
        elif self.result == "l":
            output += "{:>4s}".format("L")
        else:
            output += "    "
#            print("CODE ERROR: invalid self.result")
#            sys.exit()

        if self.stats[0] > -1:
            output += "{:6d}".format(self.stats[0])
        if self.stats[1] > -1:
            output += "{:6d}".format(self.stats[1])
        if self.stats[2] > -1:
            output += "{:4d}".format(self.stats[2])
        if self.stats[3] > -1:
            output += "{:4d}".format(self.stats[3])
        if self.stats[4] > -1:
            output += "{:4d}".format(self.stats[4]) + "{:4d}".format(sum(self.stats[1:5]))
        if self.stats[5] > -1:
            output += "{:6d}".format(self.stats[5])
        if self.stats[6] > -1:
            output += "{:6d}".format(self.stats[6])
        if self.stats[7] > -1:
            output += "{:6d}".format(self.stats[7])
        
        return output
    

#####PROGRAM#START#########################################################################################################################################        
if os.path.isfile("PandemicSessions.pkl"):
    with open("PandemicSessions.pkl","rb") as handle:
        sessions = pickle.load(handle)
else:
    sessions = []
    
# Main menu.
loop = True
while loop:
    print(str(len(sessions)) + " sessions in the logs.")
    print("What would you like to do?")
    print(" > [L]og a game session")
    print(" > [S]tatisticulate")
    print(" > [P]artnerships")
    print(" > [4]-player teams")
    print(" > [W]rite sessions")
    print(" > [C]lear sessions")
    print(" > [Q]uit")
    print
    menu_input = raw_input()
    if menu_input != "":
        menu_input = menu_input[0].lower()
    
    # Log a game session.
    if menu_input == "l":
        session = cSession()

        x = -1
        while x != 0:
            session_input = raw_input("    Number of players: ")
            x = session.set_players(session_input)
        role_num = 1
        while role_num <= session.get_players():
            session_input = raw_input("    Enter role " + str(role_num) + ": ")
            x = session.set_role(role_num,session_input)
            if x == 0:
                print(session.print_session())
                session.print_session()
                role_num += 1

        x = -1
        while x != 0:
            session_input = raw_input("    Did you [W]in or [L]ose? ")
            x = session.set_result(session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Player cards remaining:         ")
            x = session.set_stat(0,session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Blue disease cubes remaining:   ")
            x = session.set_stat(1,session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Yellow disease cubes remaining: ")
            x = session.set_stat(2,session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Black disease cubes remaining:  ")
            x = session.set_stat(3,session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Red disease cubes remaining:    ")
            x = session.set_stat(4,session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Research stations remaining:    ")
            x = session.set_stat(5,session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Outbreaks triggered:            ")
            x = session.set_stat(6,session_input)
        print(session.print_session())
        x = -1
        while x != 0:
            session_input = raw_input("    Infection level:                ")
            x = session.set_stat(7,session_input)

        print
        print(session.print_session())
        print
        valid = False
        while not valid:
            confirm_input = raw_input("Do you want to [L]og this session or [R]eturn to menu? ")
            if confirm_input != "":
                confirm_input = confirm_input[0].lower()
                if confirm_input == "l":
                    valid = True
                    sessions.append(session)
                    with open("PandemicSessions.pkl","wb") as handle:
                        pickle.dump(sessions,handle)
                    print("Session #" + str(len(sessions)) + " has been logged.")
                elif confirm_input == "r":
                    valid = True
            if not valid:
                print("ERROR: invalid input")

                
    # Statistculate: generate statistics from the logged games.
    elif menu_input == "s":
        for num_players in [3,4]:
            role_str = "{:>" + str(max( [len(role) for role in role_list] )) + "}"
#            print(role_str.format("ROLE")
            print(str(num_players) + " PLAYERS:       ROLE"
                  + "{:>6s}".format("P") + "{:>6s}".format("W") + "{:>6s}".format("L") + "{:>9s}".format("%")
                  + "{:>8s}".format("CARDS") + "{:>9s}".format("CUBES") + "{:>8s}".format("O/B") + "{:>6s}".format("ERAD") )
            print("-"*80)
            
            # Distribute the data to the individual roles present in each session.
            p_vec = [0]*len(role_list)
            w_vec = [0]*len(role_list)
            pc_vec = [0]*len(role_list)
            ct_vec = [0]*len(role_list)
            ob_vec = [0]*len(role_list)
            er_vec = [0]*len(role_list)
            for i,session in enumerate(sessions):
                if session.get_players() == num_players:
                    for role_num in range(session.get_players()):
                        role_i = role_list.index(session.get_role_by_number(role_num+1))
                        p_vec[role_i] += 1
                        if session.get_result() == "w":
                            w_vec[role_i] += 1
                        pc_vec[role_i] += session.get_player_cards()
                        ct_vec[role_i] += session.get_cubes_blue() + session.get_cubes_yellow() + session.get_cubes_black() + session.get_cubes_red()
                        ob_vec[role_i] += session.get_outbreaks()
                        er_vec[role_i] += (session.get_cubes_blue()==24) + (session.get_cubes_yellow()==24) + (session.get_cubes_black()==24) + (session.get_cubes_red()==24)

            # Calculate averages and sort the roles by winning percentage.            
            pc_vec = [float(pc_vec[i])/float(max(1,p_vec[i])) for i in range(len(role_list))]
            ct_vec = [float(ct_vec[i])/float(max(1,p_vec[i])) for i in range(len(role_list))]
            ob_vec = [float(ob_vec[i])/float(max(1,p_vec[i])) for i in range(len(role_list))]
            wl_vec = [float(w_vec[i])/float(max(1,p_vec[i]))*100. for i in range(len(role_list))]
            i_vec = sorted(range(len(role_list)), key=lambda x:wl_vec[x], reverse=True)
            
            for i in i_vec:
                print(role_str.format(role_list[i].title())
                      + "{:6d}".format(p_vec[i]) + "{:6d}".format(w_vec[i]) + "{:6d}".format(p_vec[i]-w_vec[i]) + "{:9.2f}".format(wl_vec[i])
                      + "{:8.2f}".format(pc_vec[i]) + "{:9.2f}".format(ct_vec[i]) + "{:8.2f}".format(ob_vec[i]) + "{:6d}".format(er_vec[i]) )
            print("-"*80)
            p, w = sum(p_vec)/4, sum(w_vec)/4
            print(role_str.format("TOTAL")
                  + "{:6d}".format(p) + "{:6d}".format(w) + "{:6d}".format(p-w) + "{:9.2f}".format(float(w)/float(max(1,p))*100.)
                  + "{:8.2f}".format(sum(pc_vec)/7.) + "{:9.2f}".format(sum(ct_vec)/7.) + "{:8.2f}".format(sum(ob_vec)/7.) + "{:6d}".format(sum(er_vec)/4) )
            print

        # Sort data by winnning games and losing games.
        pc, cb,cy,ck,cr,ct, rs,ob,il = [[],[]], [[],[]],[[],[]],[[],[]],[[],[]],[[],[]], [[],[]],[[],[]],[[],[]]
        for session in sessions:
            if session.get_result() == "w":
                wl = 0
            else:
                wl = 1
                
            pc[wl].append(session.get_player_cards())
            cb[wl].append(session.get_cubes_blue())
            cy[wl].append(session.get_cubes_yellow())
            ck[wl].append(session.get_cubes_black())
            cr[wl].append(session.get_cubes_red())
            ct[wl].append(cb[wl][-1]+cy[wl][-1]+ck[wl][-1]+cr[wl][-1])
            rs[wl].append(session.get_research_stations())
            ob[wl].append(session.get_outbreaks())
            il[wl].append(session.get_infection_levels())
            
        print
        print("                            " + "{:>9s}".format("WINS") + "{:>9s}".format("LOSSES") + "{:>9s}".format("TOTAL"))
        print("     Player cards remaining:" + "{:9.2f}".format(mean(pc[0])) + "{:9.2f}".format(mean(pc[1])) + "{:9.2f}".format(mean(pc[0]+pc[1])))
        print("       Blue cubes remaining:" + "{:9.2f}".format(mean(cb[0])) + "{:9.2f}".format(mean(cb[1])) + "{:9.2f}".format(mean(cb[0]+cb[1])))
        print("     Yellow cubes remaining:" + "{:9.2f}".format(mean(cy[0])) + "{:9.2f}".format(mean(cy[1])) + "{:9.2f}".format(mean(cy[0]+cy[1])))
        print("      Black cubes remaining:" + "{:9.2f}".format(mean(ck[0])) + "{:9.2f}".format(mean(ck[1])) + "{:9.2f}".format(mean(ck[0]+ck[1])))
        print("        Red cubes remaining:" + "{:9.2f}".format(mean(cr[0])) + "{:9.2f}".format(mean(cr[1])) + "{:9.2f}".format(mean(cr[0]+cr[1])))
        print("      Total cubes remaining:" + "{:9.2f}".format(mean(ct[0])) + "{:9.2f}".format(mean(ct[1])) + "{:9.2f}".format(mean(ct[0]+ct[1])))
        print("Research stations remaining:" + "{:9.2f}".format(mean(rs[0])) + "{:9.2f}".format(mean(rs[1])) + "{:9.2f}".format(mean(rs[0]+rs[1])))
        print("        Outbreaks triggered:" + "{:9.2f}".format(mean(ob[0])) + "{:9.2f}".format(mean(ob[1])) + "{:9.2f}".format(mean(ob[0]+ob[1])))
        print("            Infection level:" + "{:9.2f}".format(mean(il[0])) + "{:9.2f}".format(mean(il[1])) + "{:9.2f}".format(mean(il[0]+il[1])))


        plt.figure(1)
        plt.subplot(121)
        colours = ["cyan", "magenta", "orangered", "lime", "darkgreen", "sienna", "white"]
        plt.xlabel("Average number of cubes remaining")
        plt.ylabel("Average number of cards remaining")
        for i in range(len(role_list)):
            plt.plot(ct_vec[i],pc_vec[i], "o", mfc=colours[i],ms=20, label=role_list[i].title())
#            if ct_vec[i] < mean(ct_vec):
#                plt.annotate(role_list[i].title(), xy=(ct_vec[i],pc_vec[i]), xytext=(ct_vec[i]-0.1,pc_vec[i]-0.05), ha="right",va="top")
#            else:
#                plt.annotate(role_list[i].title(), xy=(ct_vec[i],pc_vec[i]), xytext=(ct_vec[i]+0.1,pc_vec[i]+0.05))
            plt.annotate(role_list[i].title(), xy=(ct_vec[i],pc_vec[i]), xytext=(ct_vec[i]+0.1,pc_vec[i]+0.05))
        #plt.xlim( [plt.xlim()[0]-3., plt.xlim()[1]+1.5] )
        #plt.ylim( [plt.ylim()[0]-0.5, plt.ylim()[1]+0.5] )
        plt.xlim([56,66])
        plt.ylim([5,9])
        xl,xc,xr = plt.xlim()[0], mean(ct_vec), plt.xlim()[1]
        yb,yc,yt = plt.ylim()[0], mean(pc_vec), plt.ylim()[1]
        plt.arrow( xl,yc, xr-xl-0.1,0, head_width=0.05,head_length=0.1, color="grey")
        plt.arrow( xc,yb, 0,yt-yb-0.05, head_width=0.1,head_length=0.05, color="grey")
        plt.text(xr,yc,"Better for removing cubes", ha="right",va="bottom", color="grey")
        plt.text(xc,yt,"Better for curing diseases", ha="right",va="top",rotation="vertical", color="grey")


        plt.subplot(122)
        plt.grid()
        colours = ["darkmagenta", "darkblue", "darkcyan", "darkgreen", "greenyellow", "gold", "orangered", "darkred", "black"]
        plt.xlabel("Number of cubes remaining")
        plt.xlim([20,100])
        plt.xticks(range(20,101,10))
        plt.ylabel("Number of player cards remaining")
        plt.ylim([0,max(pc[0]+pc[1])+1])
        plt.yticks(range(1,max(pc[0]+pc[1])+1,2))
        
        for outbreaks in range(9):
            indices = [i for i,j in enumerate(ob[0]+ob[1]) if j==outbreaks]
            x = [(ct[0]+ct[1])[i] for i in indices]
            y = [(pc[0]+pc[1])[i] for i in indices]
            plt.plot(x,y, "s", mew=0,mfc=colours[outbreaks],ms=9, label=str(outbreaks))

            for i in indices:
                if (cb[0]+cb[1])[i] == 24:
                    plt.plot((ct[0]+ct[0])[i], (pc[0]+pc[0])[i], marker=5,mec="white",mfc="blue")
                if (cy[0]+cy[1])[i] == 24:
                    plt.plot((ct[0]+ct[0])[i], (pc[0]+pc[0])[i], marker=6,mec="white",mfc="yellow")
                if (ck[0]+ck[1])[i] == 24:
                    plt.plot((ct[0]+ct[0])[i], (pc[0]+pc[0])[i], marker=7,mec="white",mfc="black")
                if (cr[0]+cr[1])[i] == 24:
                    plt.plot((ct[0]+ct[0])[i], (pc[0]+pc[0])[i], marker=4,mec="white",mfc="red")

        plt.plot(ct[1],pc[1], "kx",mew=2,ms=12, label="L")
        plt.legend(loc="upper left", numpoints=1)
        x = plt.get_current_fig_manager()
        x.window.state("zoomed")
        plt.show()

        
    # Rank the possible 4-player teams.
    elif menu_input == "4":
        quad_list = []
        for i1 in range(7):
            role1 = role_list[i1]
            for i2 in range(i1+1,7):
                role2 = role_list[i2]
                for i3 in range(i2+1,7):
                    role3 = role_list[i3]
                    for i4 in range(i3+1,7):
                        role4 = role_list[i4]
                        quad_list.append([role1,role2,role3,role4])
        quad_count = [0 for i in range(len(quad_list))]
        win_count = [0 for i in range(len(quad_list))]

        i1=0
        for session in sessions:
            if session.get_players() == 4:
                i1+=1
                session_list = [session.get_role_by_number(1), session.get_role_by_number(2), session.get_role_by_number(3), session.get_role_by_number(4)]
                session_list.sort()

                quad_count[ quad_list.index(session_list) ] += 1
                if session.get_result() == "w":
                    win_count[ quad_list.index(session_list) ] += 1

        for i,roles in enumerate(quad_list):
#            print( "{:2d}".format(quad_count[i]) + " : " + "/".join([role[0:3].title() for role in roles]) )
            print( "{:>4s}".format(roles[0][0:3].title()) + "{:>4s}".format(roles[1][0:3].title()) + "{:>4s}".format(roles[2][0:3].title()) + "{:>4s}".format(roles[3][0:3].title())
                   + "{:6d}".format(quad_count[i]) + "{:6d}".format(win_count[i]) + "{:6d}".format(quad_count[i]-win_count[i]) )
                   
        print(str(sum(quad_count)) + " in total.")
            

    # Rank the best partnerships.
    elif menu_input == "p":
        p_matrix = [[0 for i in range(len(role_list))] for j in range(len(role_list))]
        w_matrix = [[0 for i in range(len(role_list))] for j in range(len(role_list))]
        pc_matrix = [[0 for i in range(len(role_list))] for j in range(len(role_list))]
        ct_matrix = [[0 for i in range(len(role_list))] for j in range(len(role_list))]

        for session in sessions:
            session_roles = [session.get_role_by_number(1), session.get_role_by_number(2), session.get_role_by_number(3), session.get_role_by_number(4)]

            for i in range(0,4):
                for j in range(i+1,4):
                    ind_i = role_list.index(session_roles[i])
                    ind_j = role_list.index(session_roles[j])
                    p_matrix[ind_i][ind_j] += 1
                    if session.get_result() == 'w':
                        w_matrix[ind_i][ind_j] += 1
                    pc_matrix[ind_i][ind_j] += session.get_player_cards()
                    ct_matrix[ind_i][ind_j] += session.get_cubes_total()

        role_len = 0
        p_vector = [0 for i in range(len(role_list))]
        w_vector = [0 for i in range(len(role_list))]
        pc_vector = [0 for i in range(len(role_list))]
        ct_vector = [0 for i in range(len(role_list))]
        for i,role in enumerate(role_list):
            role_len = max(role_len,len(role))
            for j,role in enumerate(role_list):
                p_vector[i]  += p_matrix[i][j]  + p_matrix[j][i]
                w_vector[i]  += w_matrix[i][j]  + w_matrix[j][i]
                pc_vector[i] += pc_matrix[i][j] + pc_matrix[j][i]
                ct_vector[i] += ct_matrix[i][j] + ct_matrix[j][i]
            pc_vector[i] = float(pc_vector[i]) / float(p_vector[i])
            ct_vector[i] = float(ct_vector[i]) / float(p_vector[i])

        for i,role_i in enumerate(role_list):
            print(role_i.upper())
            for j,role_j in enumerate(role_list):
                if i <> j:
                    print("{:>s}".format(role_j.title()))
            

    elif menu_input == "dskgjsdp":
        role_list_len = [len(role) for role in role_list]
        role_list_len.sort()
        role_len = "{:>" + str(role_list_len[-1] + 1 + role_list_len[-2]) + "s}"
        print(role_len.format("ROLE") + "{:>6s}".format("P") + "{:>6s}".format("W") + "{:>9s}".format("%"))

        p_matrix = [[0 for i in range(len(role_list))] for j in range(len(role_list))]
        w_matrix = [[0 for i in range(len(role_list))] for j in range(len(role_list))]
        for session in sessions:    
            for i in range(4):
                role_i = session.get_role_by_number(i+1)
                index_i = role_list.index(role_i)
                for j in range(i+1,4):
                    role_j = session.get_role_by_number(j+1)
                    index_j = role_list.index(role_j)
                    
                    p_matrix[index_i][index_j] += 1
                    if session.get_result() == "w":
                        w_matrix[index_i][index_j] += 1

        partnership_matrix = []
        for i in range(len(role_list)):
            for j in range(i+1,len(role_list)):
                p = p_matrix[i][j] + p_matrix[j][i]
                w = w_matrix[i][j] + w_matrix[j][i]
                partnership_matrix.append([role_list[i].title(),role_list[j].title(), p,w, float(w)/float(p)*100.])
        partnership_matrix.sort(key=lambda x: x[4], reverse=True)
        for row in partnership_matrix:
            print(role_len.format("/".join(row[0:2])) + "{:6d}".format(row[2]) + "{:6d}".format(row[3]) + "{:9.2f}".format(row[4]))

                
    # Write sessions to screen.
    elif menu_input == "w":
        print_input = raw_input("Input a comma-separated list of the sessions you wish to print, or leave blank to print all. ")
        if print_input == "":
            print_input = range(1,len(sessions)+1)
        else:
            temp = print_input.split(",")
            print_input = [int(x) for x in temp if x.isdigit()]
        print(print_input)
        for session_num in print_input:
            if 1 <= session_num <= len(sessions):
                print_output = sessions[session_num-1].print_session()
                print( "{:4d}".format(session_num) + print_output )
            else:
                print("ERROR: session #" + str(session_num) + " is not on record.")

                
    # Clear specific sessions.
    elif menu_input == "c":
        print_input = raw_input("Input a comma-separated list of the sessions you wish to clear, or leave blank to clear all. ")
        if print_input == "":
            print_input = range(1,len(sessions)+1)
        else:
            temp = print_input.split(",")
            print_input = [int(x) for x in temp if x.isdigit()]
        print(print_input)
        print_input.sort(reverse=True)
        for session_num in print_input:
            if 1 <= session_num <= len(sessions):
                sessions.pop(session_num-1)
            else:
                print("ERROR: session #" + str(session_num) + " is not on record.")

                
    # Quit.
    elif menu_input == "q" or menu_input == "":
        loop = False

        
    print
