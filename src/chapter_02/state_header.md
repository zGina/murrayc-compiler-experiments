## scanner

### state descriptor / Class State 
* nfa
<center> 

![NFA](/compiler/murrayc-compiler-experiments/src/chapter_02/imgs/nfa.png) 
 </center>

* dfa
<center> 

![NFA](/compiler/murrayc-compiler-experiments/src/chapter_02/imgs/dfa.png) 
 </center>

* minimal_dfa
<center> 

![NFA](/compiler/murrayc-compiler-experiments/src/chapter_02/imgs/minimal_dfa.png) 
 </center>
#### property
private:

* string id_;
* bool accepting_ = false;
* unordered_map<char, States> states_;

public:

* const char E='#'; // epilson
  
#### operation
public:

* add states
  * Add a state 
    

    ```
    std::shared_ptr<State>  // maybe to itself
    add(char_t ch, const std::shared_ptr<State>& state) {
    states_[ch].emplace(state);
    return state;
    }
    ```

    ```
    std::shared_ptr<State>  // to the next state
    add(char_t ch, const std::string& id, bool accepting = false)
    {
    auto s = std::make_shared<State>(id, accepting);
    return add(ch, s);
    }
    ```
   * why don't emerge them?
    

* find next_states
  * Get all states reachable via @ch
  
    ```
     auto next_states(char ch) {
    auto iter = states_.find(ch);
    if (iter == std::end(states_)) {
      return States();
    }

    return iter->second;
    }
    ```
  * Get all states reachable via any chars
  
    ```
    auto next_states(char ch) {
    auto iter = states_.find(ch);
    if (iter == std::end(states_)) {
      return States();
    }
    return iter->second;
    }
    ```
  * Get states via e
    ```
    next_states_via_e() {
    return next_states(State::E);
    }
    ```

####　```shared_ptr```
* 智能指针，多个　shared_ptr　对象可占有同一对象
####　```emplace```


####　```explicit```



####　```constexpr```
